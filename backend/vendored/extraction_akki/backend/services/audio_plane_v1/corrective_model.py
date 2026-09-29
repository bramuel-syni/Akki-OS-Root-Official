"""Local Whisper encoder-LoRA + speaker-adversarial bottleneck; every trainable path is privatized."""
import torch
from torch import nn
from peft import LoraConfig, get_peft_model
from transformers import WhisperModel

FRAMES = 200  # the declared two-second window at Whisper's 10 ms hop


class Reverse(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x, coefficient):
        ctx.coefficient = coefficient
        return x.view_as(x)

    @staticmethod
    def backward(ctx, gradient):
        return -ctx.coefficient * gradient, None


class CorrectiveModel(nn.Module):
    def __init__(self, local_path, languages, presenters, control):
        super().__init__()
        base = WhisperModel.from_pretrained(local_path, local_files_only=True).encoder
        for p in base.parameters():
            p.requires_grad = False
        # A declared two-second encoder, not 28 seconds of padded work per two-second window.
        base.config.max_source_positions = FRAMES // 2
        base.embed_positions = nn.Embedding.from_pretrained(base.embed_positions.weight[:FRAMES // 2].detach().clone(), freeze=True)
        self.encoder = get_peft_model(base, LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05,
                                                     target_modules=['q_proj', 'v_proj'], bias='none'))
        dim = control.get('bottleneck_dim', 128)
        self.project = nn.Sequential(nn.LayerNorm(base.config.d_model), nn.Linear(base.config.d_model, dim), nn.GELU())
        self.language_head = nn.Linear(dim, languages)
        self.speaker_head = nn.Linear(dim, presenters)
        self.condition_head = nn.Linear(dim, control['condition_count'])
        self.adversary_strength = control['adversary_strength']
        self.bottleneck_noise = control.get('bottleneck_noise', 0.0)

    def forward(self, features):
        enc = self.encoder(input_features=features).last_hidden_state.mean(1)
        z = self.project(enc)
        if self.training and self.bottleneck_noise > 0:
            # Capacity limit on the bottleneck: what a probe can read from z is bounded by this noise floor.
            z = z + torch.randn_like(z) * self.bottleneck_noise
        reversed_z = Reverse.apply(z, self.adversary_strength)
        return self.language_head(z), self.speaker_head(reversed_z), self.condition_head(reversed_z), z, enc


class Featurizer:
    """Whisper log-mel computed on the device over exactly the two-second window.

    Same STFT/filterbank/log/clamp arithmetic as the pretrained extractor, without padding every
    clip to thirty seconds on the CPU first: the input pipeline no longer starves the GPU.
    """

    def __init__(self, processor, device):
        extractor = processor.feature_extractor
        self.n_fft, self.hop, self.device = extractor.n_fft, extractor.hop_length, device
        self.window = torch.hann_window(extractor.n_fft, device=device)
        self.filters = torch.from_numpy(extractor.mel_filters).to(device, torch.float32).T.contiguous()

    def __call__(self, pcm, augment=False):
        wave = pcm.to(self.device, non_blocking=True).to(torch.float32) / 32767.0
        stft = torch.stft(wave, self.n_fft, self.hop, window=self.window, return_complex=True)
        magnitudes = stft[..., :-1].abs() ** 2
        log_spec = torch.clamp(self.filters @ magnitudes, min=1e-10).log10()
        log_spec = torch.maximum(log_spec, log_spec.amax(dim=(1, 2), keepdim=True) - 8.0)
        features = ((log_spec + 4.0) / 4.0)[:, :, :FRAMES]
        if augment:
            features = augment_batch(features)
        return features


def augment_batch(features):
    """Training-only recording-condition perturbation, vectorised over the batch; no test augmentation or relabelling."""
    n, f, t = features.shape
    features = features + torch.randn_like(features) * 0.02
    f0 = torch.randint(0, 73, (n, 1, 1), device=features.device)
    t0 = torch.randint(0, 181, (n, 1, 1), device=features.device)
    fi = torch.arange(f, device=features.device).view(1, f, 1)
    ti = torch.arange(t, device=features.device).view(1, 1, t)
    mask = ((fi >= f0) & (fi < f0 + 8)) | ((ti >= t0) & (ti < t0 + 20))
    return torch.where(mask, features.mean(dim=(1, 2), keepdim=True), features)

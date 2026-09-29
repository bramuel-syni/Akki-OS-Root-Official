"""Local Whisper encoder-LoRA + speaker-adversarial bottleneck; every trainable path is privatized."""
import torch
from torch import nn
from peft import LoraConfig, get_peft_model
from transformers import WhisperModel


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
        base.config.max_source_positions = 100
        base.embed_positions = nn.Embedding.from_pretrained(base.embed_positions.weight[:100].detach().clone(), freeze=True)
        self.encoder = get_peft_model(base, LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05,
                                                     target_modules=['q_proj', 'v_proj'], bias='none'))
        self.project = nn.Sequential(nn.LayerNorm(base.config.d_model), nn.Linear(base.config.d_model, 128), nn.GELU())
        self.language_head = nn.Linear(128, languages)
        self.speaker_head = nn.Linear(128, presenters)
        self.condition_head = nn.Linear(128, control['condition_count'])
        self.adversary_strength = control['adversary_strength']

    def forward(self, features):
        enc = self.encoder(input_features=features).last_hidden_state.mean(1)
        z = self.project(enc)
        reversed_z = Reverse.apply(z, self.adversary_strength)
        return self.language_head(z), self.speaker_head(reversed_z), self.condition_head(reversed_z), z, enc


def mel_batch(processor, pcm, device, augment=False):
    import numpy as np
    arr = pcm.numpy().astype(np.float32) / 32767.0
    features = processor.feature_extractor(list(arr), sampling_rate=16000, return_tensors='pt', device=device).input_features
    features = features[:, :, :200].to(device)
    if augment:
        # Only the training path changes recording conditions; no test augmentation or relabelling.
        features = features + torch.randn_like(features) * 0.02
        for sample in features:
            f = int(torch.randint(0, 73, ())); t = int(torch.randint(0, 181, ()))
            sample[f:f + 8, :] = sample.mean()
            sample[:, t:t + 20] = sample.mean()
    return features
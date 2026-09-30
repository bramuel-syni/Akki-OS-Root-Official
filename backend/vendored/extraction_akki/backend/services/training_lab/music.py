"""Speech/music are independent events. Thresholds must be calibrated, never guessed."""
import math


def classify_events(speech, music, *, speech_threshold, music_threshold, calibration_ref):
    for value in (speech,music,speech_threshold,music_threshold):
        if not isinstance(value,(int,float)) or isinstance(value,bool) or not math.isfinite(value) or not 0 <= value <= 1:
            raise ValueError("Finite probabilities and calibrated thresholds required")
    if not calibration_ref:
        raise ValueError("Calibration reference required")
    has_speech,has_music = speech >= speech_threshold, music >= music_threshold
    return {"label":"mixed" if has_speech and has_music else "speech" if has_speech else "music" if has_music else "unknown",
            "speech_probability":speech,"music_probability":music,"calibration_ref":calibration_ref,
            "evidence_class":"caller_supplied_probabilities_not_verified_inference"}


def make_music_head(feature_width):
    """Host-only trainable multi-label head; no pretrained/admitted weight claim."""
    from torch import nn
    return nn.Linear(feature_width, 2)
from numpy.typing import NDArray
import torch
from TTS.api import TTS
import numpy as np

def quotes_to_audio(quotes: list[str], presenter_audio: str,
    pause_seconds: int = 1.0) -> tuple[NDArray, int]:
        device = "cuda" if torch.cuda.is_available() else "cpu"    
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
        sample_rate = 24_000  # tts default sample rate
        audio_segments = []
        pause_samples = int(sample_rate * pause_seconds)
        total_samples = 0
        for quote in quotes:
            wav = tts.tts(text=quote, speaker_wav=presenter_audio, language="en")
            wav = np.array(wav)
            total_samples += wav.shape[0]
            audio_segments.append(wav)
        combined_wav = np.zeros(total_samples + (len(audio_segments) - 1) * pause_samples)
        idx = 0
        for segment in audio_segments:
            end_of_segment = idx + segment.shape[0]
            combined_wav[idx:end_of_segment] = segment
            idx = end_of_segment + pause_samples
        return combined_wav, sample_rate

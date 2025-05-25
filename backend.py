# backend.py

import whisper

# Load the model only once (at module level, not every function call)
model = whisper.load_model("medium")  # You can change 'medium' to another model if needed

import torch
print("CUDA available:", torch.cuda.is_available())


def transcribe_audio_file(audio_file_path):
    """
    Transcribes the given audio file to text using the Whisper model.

    Parameters:
        audio_file_path (str): Path to the audio file (.wav, .mp3, .mp4, etc.)

    Returns:
        str: Transcribed text
    """
    result = model.transcribe(audio_file_path)
    return result["text"]

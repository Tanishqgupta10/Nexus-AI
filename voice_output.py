"""
NEXUS AI — Voice Output
Local text-to-speech using pyttsx3 / Windows SAPI.
No paid API and no cloud TTS required.
"""

import os
import tempfile
from pathlib import Path


def text_to_speech(text: str, rate: int = 175, volume: float = 1.0) -> bytes:
    """Convert text to WAV audio bytes using the local TTS engine."""
    text = str(text or "").strip()
    if not text:
        return b""

    try:
        import pyttsx3
    except ImportError as exc:
        raise RuntimeError(
            "Voice output dependency is missing. Run: pip install pyttsx3"
        ) from exc

    engine = pyttsx3.init()
    engine.setProperty("rate", rate)
    engine.setProperty("volume", volume)

    with tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False,
    ) as tmp:
        output_path = tmp.name

    try:
        engine.save_to_file(text, output_path)
        engine.runAndWait()
        engine.stop()

        path = Path(output_path)
        if not path.exists():
            raise RuntimeError("The local TTS engine did not create an audio file.")

        return path.read_bytes()
    finally:
        Path(output_path).unlink(missing_ok=True)


def clean_for_speech(text: str) -> str:
    """Remove common Markdown/UI syntax before speaking."""
    text = str(text or "")
    text = text.replace("```", " ")
    text = text.replace("**", "")
    text = text.replace("__", "")
    text = text.replace("###", "")
    text = text.replace("##", "")
    text = text.replace("#", "")
    text = text.replace("`", "")
    text = text.replace("—", "-")
    return " ".join(text.split())

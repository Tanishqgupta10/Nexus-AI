"""
NEXUS AI — Voice Input 4.0
Windows-safe local speech-to-text with faster-whisper.

Fixes OpenMP runtime conflict that can crash Streamlit when Whisper starts.
"""

import os

# IMPORTANT:
# faster-whisper/ctranslate2 can load Intel OpenMP while another dependency
# has already loaded a second OpenMP runtime. On Windows this can terminate
# the Python process with OMP Error #15.
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
os.environ.setdefault("OMP_NUM_THREADS", "4")

import tempfile
from pathlib import Path

import streamlit as st


@st.cache_resource(show_spinner=False)
def _load_whisper_model(model_size="tiny"):
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise RuntimeError(
            "Voice dependencies are missing. Run:\n"
            "pip install audio-recorder-streamlit faster-whisper"
        ) from exc

    return WhisperModel(
        model_size,
        device="cpu",
        compute_type="int8",
        cpu_threads=4,
        num_workers=1,
    )


def transcribe_audio(audio_bytes, model_size="tiny"):
    """Transcribe microphone audio without VAD filtering."""

    if not audio_bytes:
        return ""

    if len(audio_bytes) < 2000:
        raise RuntimeError(
            "Recording is too short. Hold Start Voice Chat and "
            "speak clearly for 2–5 seconds."
        )

    audio_path = None

    try:
        model = _load_whisper_model(model_size)

        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False,
        ) as tmp:
            tmp.write(audio_bytes)
            audio_path = tmp.name

        segments, info = model.transcribe(
            audio_path,
            beam_size=1,
            best_of=1,
            temperature=0,
            condition_on_previous_text=False,
            vad_filter=False,
            language=None,
        )

        parts = []

        for segment in segments:
            value = segment.text.strip()
            if value:
                parts.append(value)

        result = " ".join(parts).strip()

        if not result:
            raise RuntimeError(
                "Whisper received the recording but recognized no speech. "
                "Try speaking closer to the microphone for 2–5 seconds."
            )

        return result

    except RuntimeError:
        raise
    except Exception as exc:
        raise RuntimeError(
            f"Voice transcription failed: {exc}"
        ) from exc
    finally:
        if audio_path:
            Path(audio_path).unlink(missing_ok=True)

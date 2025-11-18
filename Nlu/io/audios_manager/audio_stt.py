# io/audios_manager/audio_stt.py
import os
from faster_whisper import WhisperModel

"""
audio_stt.py — Módulo de transcripción de voz a texto
------------------------------------------------------
Convierte archivos de audio (ogg, wav, mp3, etc.)
en texto legible que el NLU pueda interpretar.

Depende de:
 - faster-whisper
 - ffmpeg (binario en /tools/ffmpeg/bin/)
"""

# =========================================================
# ⚙️ CONFIGURACIÓN INICIAL
# =========================================================
# Ruta al binario de ffmpeg (para asegurar compatibilidad en Windows)
ffmpeg_dir = os.path.abspath("tools/ffmpeg/bin")
os.environ["PATH"] = ffmpeg_dir + ";" + os.environ["PATH"]

# Carga del modelo Whisper
# Modelos disponibles: tiny, base, small, medium, large
model = WhisperModel("small", device="cpu", compute_type="int8")

# =========================================================
# 🎙️ FUNCIÓN PRINCIPAL
# =========================================================
def transcribe_audio(audio_path: str) -> str:
    """
    Transcribe un archivo de audio y devuelve el texto en español.
    audio_path → ruta del archivo de audio (ogg, wav, mp3…)
    """
    if not os.path.exists(audio_path):
        print(f"[x] No se encontró el archivo: {audio_path}")
        return ""

    print(f"[🎧] Transcribiendo: {audio_path} ...")

    # Transcripción con configuración ligera (optimizada para ATLAS)
    segments, info = model.transcribe(
        audio_path,
        vad_filter=True,               # filtra silencios automáticos
        beam_size=1,                   # velocidad > precisión
        condition_on_previous_text=False,
        language="es",
        task="transcribe"
    )

    # Unir los segmentos de texto
    texto = "".join(seg.text for seg in segments).strip()

    print(f"[✓] Texto detectado: {texto}")
    print(f"[i] Idioma: {info.language} (confianza: {info.language_probability:.2f})")

    return texto


# =========================================================
# 🧩 PRUEBA RÁPIDA
# =========================================================
if __name__ == "__main__":
    # Ejemplo: transcribir un audio guardado en audios_raw
    prueba = "io/audios_manager/audios_raw/Audio1.ogg"
    texto_resultante = transcribe_audio(prueba)
    print("\nTexto final:", texto_resultante)

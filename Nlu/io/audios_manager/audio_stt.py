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

#Esto es para solucionar un error con windoes aunqe tengo entendido que el error no aparece en todas las compus(creo que depende de la version de windous)
ffmpeg_dir = os.path.abspath("tools/ffmpeg/bin")
os.environ["PATH"] = ffmpeg_dir + ";" + os.environ["PATH"]

# Carga el modelo fast Whisper
# Todas las configuraciones posibles: tiny, base, small, medium, large
#Elegi la small porque de todas las pruebas que hice es la mejor calida/velocidad
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

    # Configuracion para que sea rapida
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


#Test
if __name__ == "__main__":
    # Ejemplo: transcribir un audio guardado en audios_raw
    prueba = "io/audios_manager/audios_raw/Audio1.ogg"
    texto_resultante = transcribe_audio(prueba)
    print("\nTexto final:", texto_resultante)

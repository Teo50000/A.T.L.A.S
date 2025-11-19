import os
import torch
from faster_whisper import WhisperModel


ffmpeg_path = os.path.abspath("bin")
os.environ["PATH"] = ffmpeg_path + ";" + os.environ["PATH"]

if torch.cuda.is_available():
    device = "cuda"           # GPU Nvidia
    compute_type = "float16"
elif torch.backends.mps.is_available():  # Apple M1/M2
    device = "mps"
    compute_type = "float16"
else:
    device = "cpu"            # CPU normal
    compute_type = "int8"     # Más eficiente para CPU

print(f"Usando dispositivo: {device} ({compute_type})")


model = WhisperModel("small", device=device, compute_type=compute_type)


segments, info = model.transcribe(
    "Audio4.ogg",
    vad_filter=True,
    beam_size=1,
    condition_on_previous_text=False,
    language="es",             
    task="transcribe"          
)


texto = "".join(segment.text for segment in segments)
print("Texto:", texto)


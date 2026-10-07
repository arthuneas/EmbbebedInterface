# pyrefly: ignore [missing-import]
from faster_whisper import WhisperModel
import time

# usamos modelo tiny para rodar no cpu, para rodar em placa de video usamos o modelo medium
model = WhisperModel("tiny", device = "cpu", compute_type= "int8")

start = time.time()

# segments traz uma lista das frases faladas
# info traz informações do audio

# vad_filter é um filtro que remove partes do audio que não tem falas, é bem util para quando queremos que o modelo foque so nas falas
segments, info = model.transcribe("audio.wav", vad_filter=True)

print(f"Idioma detectado: {info.language} ({info.language_probability:.2f}%)")  

final_text = ""

for segment in segments:
    #print("[%s] --> [%s] %s" % (segment.start, segment.end, segment.text))
    final_text += segment.text + " "


end = time.time()

print(f"\nTempo de execução: {end - start:.2f} segundos")
print(f"\nTexto transcrito: {final_text.strip()}")

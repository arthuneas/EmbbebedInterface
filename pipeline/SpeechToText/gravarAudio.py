import pyaudio
import wave
import os

FORMAT = pyaudio.paInt16 # formato do audio de 16 bits
CHANNELS = 1 # audio mono, se fosse estéreo seria 2
RATE = 44100 # taxa de amostragem, ou seja, quantidade de frames por segundo
CHUNK = 1024 # tamanho do buffer, ou seja, quantidade de frames por buffer
RECORD_SECONDS = 3 # tempo de gravação em segundos
WAVE_OUTPUT_FILENAME = "audio.wav" # nome do arquivo de áudio

p = pyaudio.PyAudio() #declaração da classe PyAudio

os.system('clear') # limpa a tela

print("\n[Recording]\n") # inicio da gravação

# abre a porta de áudio para gravar
stream = p.open(format=FORMAT, 
    channels=CHANNELS, 
    rate=RATE, 
    input=True, 
    frames_per_buffer=CHUNK
)

# armazenando os frames de audio
frames = []

for i in range(0, int(RATE / CHUNK) * RECORD_SECONDS):
    data = stream.read(CHUNK)
    frames.append(data)

print("\n[Finished]\n")

stream.stop_stream() # fecha os canais de audio
stream.close() # fecha o stream
p.terminate() # encerra a classe PyAudio

waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb') # abre o arquivo em modo de escrita
waveFile.setnchannels(CHANNELS) # define a quantidade de canais
waveFile.setsampwidth(p.get_sample_size(FORMAT)) # define o formato do audio
waveFile.setframerate(RATE) # define a taxa de amostragem
waveFile.writeframes(b''.join(frames)) # escreve os frames de audio no arquivo
waveFile.close() # fecha o arquivo

print(f"\nAudio salvo como {WAVE_OUTPUT_FILENAME}") # mostra o nome do arquivo
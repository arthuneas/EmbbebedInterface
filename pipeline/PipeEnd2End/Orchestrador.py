import os
import subprocess
import time
import asyncio
import io

# pyrefly: ignore[missing-import]
from dotenv import load_dotenv
load_dotenv()

# pyrefly: ignore[missing-import]
from faster_whisper import WhisperModel
# pyrefly: ignore[missing-import]
from groq import Groq
# pyrefly: ignore[missing-import]
import edge_tts
# pyrefly: ignore[missing-import]
import av

os.system('clear')

# configurações globais
DIRETORIO_ATUAL = os.path.dirname(__file__)

# Caminho do audio de pergunta (SpeechToText)
AUDIO_ENTRADA = os.path.abspath(os.path.join(DIRETORIO_ATUAL, "..", "SpeechToText", "audio.wav"))

# Caminho do audio de resposta (TextToSpeech)
AUDIO_SAIDA = os.path.abspath(os.path.join(DIRETORIO_ATUAL, "..", "TextToSpeech", "Resposta.wav"))

# VOZ NEURAL USADA (PODE SER MUDADA)
VOZ = "pt-BR-FranciscaNeural"
SAMPLE_RATE = 24000  #taxa de amostragem

# Inicialização do Cliente Groq
API_KEY = os.environ.get("GROQ_API_KEY")
cliente_groq = Groq(api_key=API_KEY)



# Função auxiliar para converter mp3 para wav
def converter_mp3_para_wav(mp3_bytes_io, caminho_wav_saida):
    """
    Pega os bytes que estão na memória RAM e grava direto em WAV PCM 16-bit 24kHz.
    (Mesmo formato que enviaremos via Wi-Fi para o ESP32 no Mês 3).
    """
    inp = av.open(mp3_bytes_io, format='mp3')
    out = av.open(caminho_wav_saida, 'w', format='wav')
    stream = out.add_stream('pcm_s16le', rate=SAMPLE_RATE, layout='mono')
    
    for frame in inp.decode(audio=0):
        frame.pts = None
        for packet in stream.encode(frame):
            out.mux(packet)
            
    for packet in stream.encode():
        out.mux(packet)
        
    out.close()
    inp.close()


# inicializações
print("[INICIALIZANDO O CÉREBRO DO ROBÔ...]\n")

model_stt = WhisperModel("tiny", device="cpu", compute_type="int8")
print("[CARREGADO]\n")

input("Pressione [ENTER] para iniciar o Pipeline...")
os.system('clear')



async def pipeline():
    
    tempo_inicio_total = time.time()

    # ---------------------------------------
    # 1. Speech to Text (gravação de audio)
    print("[1. SPEECH TO TEXT]\n")
    
    inicio_stt = time.time()

    segments, info = model_stt.transcribe(AUDIO_ENTRADA, vad_filter = True)

    ask_transcribe = ""

    for segment in segments:
        ask_transcribe += segment.text + " "

    ask_transcribe = ask_transcribe.strip()

    fim_stt = time.time()

    print(f"[TEMPO DE EXECUÇÃO STT]: {fim_stt - inicio_stt:.2f} segundos\n")
    print(f"[PERGUNTA TRANSCRITA]: {ask_transcribe}\n")
    

    time.sleep(3)
    os.system('clear')


    # ---------------------------
    # Estágio de LLM, Groq
    print("[2. LLM GROQ]\n")

    inicio_llm = time.time()

    mensagens = [
        {
            "role": "system",
            "content": "Você é um robô educacional muito simpático e prestativo. Responda a criança em no MÁXIMO 2 frases curtas e simples. É ESTRITAMENTE PROIBIDO usar emojis ou caracteres especiais, apenas texto puro."
        },
        {
            "role": "user",
            "content": ask_transcribe
        }
    ]

    response = cliente_groq.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages = mensagens,
        max_tokens = 150,
        temperature = 0.7,
    )

    awnser_text = response.choices[0].message.content
    tempo_llm = time.time() - inicio_llm

    print(f"[RESPOSTA GROQ]: {awnser_text}\n")
    print(f"[TEMPO DE EXECUÇÃO LLM]: {tempo_llm:.2f} segundos\n")


    time.sleep(3)
    os.system('clear')


    # --------------------------------
    # 3. Estágio de TTS, Edge TTS
    print("[3. TTS EDGE TTS]\n")

    inicio_tts = time.time()

    comunicador = edge_tts.Communicate(
        text = awnser_text,
        voice = VOZ,
        rate = "+15%",
        pitch = "+10Hz"
    )

    # recebe bytes na ram e salva em .wav em tempo real
    # arquivo invisível de buffer na própria ram
    MP3buffer = io.BytesIO()

    print("[GENERATING AUDIO...]")

    # recebe os chunks de dados da internet em tempo real
    async for chunk in comunicador.stream():
        if chunk["type"] == "audio":
            MP3buffer.write(chunk["data"]) #coloca os chunks em MP3buffer

    #volta para o início do arquivo virtual na memória
    MP3buffer.seek(0) 
    #converte o arquivo virtual de MP3 para WAV
    converter_mp3_para_wav(MP3buffer, AUDIO_SAIDA)

    fim_tts = time.time()
    tempo_stt = fim_stt - inicio_stt
    tempo_tts = fim_tts - inicio_tts
    
    # Latência real de resposta: soma pura dos 3 estágios de IA
    tempo_total = tempo_stt + tempo_llm + tempo_tts

    print(f"[Áudio salvo em]: {AUDIO_SAIDA}")
    print(f"[Tempo de síntese]: {tempo_tts:.2f} segundos")

    time.sleep(2)
    os.system('clear')
    
    #--------------------------------
    # 4. Relatório Final de Latência
    print("RELATÓRIO DE LATÊNCIA (PIBITI)\n")
    print("-" * 50 + "\n")

    print(f"[TEMPO STT]:              {tempo_stt:.2f} segundos\n")
    print(f"[TEMPO LLM]:              {tempo_llm:.2f} segundos\n")
    print(f"[TEMPO TTS]:              {tempo_tts:.2f} segundos\n")
    print(f"[LATÊNCIA TOTAL]:   {tempo_total:.2f} segundos\n")

    print("-" * 50 + "\n")

    if tempo_total <= 4.0:
        print("[O ROBÔ ESTÁ COM BOA LATÊNCIA! DENTRO DA META DO PIBITI]\n")
    else:
        print("[O ROBÔ ESTÁ COM LATÊNCIA ALTA, PRECISA MELHORAR!]\n")

    # Reproduz o áudio após o relatório
    if os.path.exists(AUDIO_SAIDA):
        print("[ROBÔ FALANDO...]\n")
        subprocess.run(["afplay", AUDIO_SAIDA])


if __name__ == '__main__':
    asyncio.run(pipeline())
    
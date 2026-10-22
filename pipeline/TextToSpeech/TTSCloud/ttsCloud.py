import asyncio
# pyrefly: ignore [missing-import]
import edge_tts
import subprocess
import os
import time
# pyrefly: ignore[missing-import]
import av
import io

os.system('clear')  

VOZ = "en-US-AndrewMultilingualNeural" #voz feminina amigavel
SAMPLE_RATE = 24000  #taxa de amostragem


resposta = "Oi! Eu sou o robô assistente, e estou muito feliz em poder ajudar você a resolver esse problema!"


saida = os.path.join(os.path.dirname(__file__), "respostaTTS.wav")


def convert_mp3_to_wav(mp3_bytes_io, caminho_wav_saida):
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



async def gerar_voz():
    print("[STARTING EDGE TTS...]")
    
    inicio = time.time()

    comunicador = edge_tts.Communicate(
        text = resposta,
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
    convert_mp3_to_wav(MP3buffer, saida)

    fim = time.time()

    print(f"[Áudio salvo em]: {saida}")
    print(f"[Tempo de síntese]: {fim - inicio:.2f} segundos")

    if os.path.exists(saida):
        subprocess.run(["afplay", saida])


asyncio.run(gerar_voz())


# ==============================================================================
# OPÇÕES DE VOZES NEURAIS (MICROSOFT EDGE TTS)
# ==============================================================================
# --- Vozes Nativas Brasileiras (pt-BR) ---
# "pt-BR-FranciscaNeural"           -> Feminina: calorosa, natural, amigável e expressiva (Padrão)
# "pt-BR-ThalitaMultilingualNeural" -> Feminina: jovem, dinâmica, alegre e descontraída
# "pt-BR-AntonioNeural"             -> Masculina: madura, natural, firme e simpática
#
# --- Vozes Multilíngues de Nova Geração (Falam PT-BR perfeitamente) ---
# "en-US-AvaMultilingualNeural"     -> Feminina: moderna, tom brilhante e animado
# "en-US-EmmaMultilingualNeural"    -> Feminina: suave, amigável e acolhedora
# "en-US-AndrewMultilingualNeural"  -> Masculina: jovem, expressiva e entusiasmada
# "en-US-BrianMultilingualNeural"   -> Masculina: calorosa e agradável
# "en-AU-WilliamMultilingualNeural" -> Multilíngue: descontraído, natural e expressivo
#
# --- Dicas de Personalização no Communicate() ---
# rate="+15%"   -> Aumenta a velocidade (deixa a fala mais ágil e animada)
# pitch="+5Hz"  -> Eleva o tom (deixa a voz ligeiramente mais meiga/jovem)
# ==============================================================================


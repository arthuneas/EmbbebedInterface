# pyrefly: ignore [missing-import]
from kokoro import KPipeline

# pyrefly: ignore [missing-import]
import soundfile as sf
import time
import os
import subprocess

os.system('clear')  

#configuração do kokoro tts
VOZ = 'pm_alex' #voz feminina amigavel
SAMPLE_RATE = 24000  #taxa de amostragem

print("[INICIALIZING KOKORO TTS...]\n")

#criação do pipeline do kokoro tts
pipe = KPipeline(lang_code = "pt-br")

print(f"[KOKORO TTS Inicializado]")

resposta = "oi! eu sou a sophia!, e estou muito feliz em poder ajudar você a resolver esse problema!"

saida = os.path.join(os.path.dirname(__file__), "respostaTTS.wav")

print("\n[GENERATING AUDIO...]")

inicio = time.time()

gerador = pipe(resposta, voice = VOZ, speed = 1.1)


for i, (grafema, fonema, audio) in enumerate(gerador):
    sf.write(saida, audio, SAMPLE_RATE)


fim = time.time()

print(f"\n[Áudio salvo em]: {saida}")
print(f"[Tempo de síntese]: {fim - inicio:.2f} segundos")


# reproduz o audio no macOS
if os.path.exists(saida):
    subprocess.run(["afplay", saida], check=True)
    



# ==============================================================================
# OPÇÕES DE VOZES (KOKORO TTS)
# ==============================================================================
# --- Vozes Femininas Mais Animadas e Expressivas ---
# 'af_bella'   -> Muito animada, expressiva e alegre (ótima para robôs infantis)
# 'af_heart'   -> Doce, calorosa, natural e carismática (favorita da comunidade)
# 'af_sky'     -> Jovem, dinâmica e descontraída
# 'af_sarah'   -> Entusiasmada, clara e profissional
#
# --- Vozes com Sotaque Nativo PT-BR ---
# 'pf_dora'    -> Voz feminina calma e amigável
# 'pm_alex'    -> Voz masculina jovem e natural
# 'pm_santa'   -> Voz masculina profunda e animada
#
# --- Vozes Masculinas Expressivas ---
# 'am_puck'    -> Animado, tom travesso e enérgico
# 'am_fenrir'  -> Enérgica e marcante
# ==============================================================================


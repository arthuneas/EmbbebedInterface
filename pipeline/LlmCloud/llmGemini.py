# O Gemini é uma API da Google que aceita diversos tipos de entrada. 
# Isso inclui a entrada de audio direto e via texto.getattr

# pyrefly: ignore [missing-import]
from google import genai
# pyrefly: ignore [missing-import]
from google.genai import types
import time
import os

from dotenv import load_dotenv
load_dotenv()

# conexão com a API do Google
API_KEY = os.environ.get("GEMINI_API_KEY")

# inicializa a API do Google
client = genai.Client(api_key=API_KEY)

os.system('clear')

prompt = 'Qual o ultimo album da ariana grande?'

# aqui adicionamos a personalidade do robô usando o System Prompt dentro de uma configuração
config_internet = types.GenerateContentConfig(
    system_instruction = 'Você é um robô educacional super amigável e feliz. Responda a criança em no máximo 3 frases curtas.',
    temperature = 0.8, # qual criativo deve ser o robô   
    tools = [{"google_search" : {}}] #pesquisa em tempo real
)


config_offline = types.GenerateContentConfig(
    system_instruction = 'Você é um robô educacional super amigável e feliz. Responda a criança em no máximo 3 frases curtas.',
    temperature = 0.8, # qual criativo deve ser o robô   
)

start = time.time()

print("[Sending To Gemini API...]")


try:
    #primeiro tenta rodar o modelo com internet
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents = prompt,
        config = config_internet
    )

except Exception as error:
    print(f"Limite Atingido!")
    #Without Internet, Switching To Offline Model
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents = prompt,
        config = config_offline
    )


end = time.time()

print(f"\n[Gemini Processing Time]: {end - start:.2f} seconds")
print(f"\n[Gemini Response]: {response.text}")
    
import time
import os
# pyrefly: ignore [missing-import]
from groq import Groq
# pyrefly: ignore [missing-import]
from ddgs import DDGS
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.environ.get("GROQ_API_KEY")

client = Groq(api_key = API_KEY)

os.system('clear')

prompt = 'me fale sobre o capítulo 2 de deltarune'

# calculando todo o tempo de rota.
start = time.time()


# Busca na internet para atualização de respostas
print("[Searching On Internet...]")

resultados = ""

try: 
    with DDGS() as ddgs:
        # 1ª Economia: Pegar apenas os 2 primeiros links em vez de 3
        results = ddgs.text(prompt, max_results=2)
        for r in results:
            resultados += r['body'] + " "
            
        # 2ª Economia (A mais importante): Limitar o texto a 400 caracteres
        # Isso garante que não vai estourar os tokens de Input.
        resultados = resultados[:600]
except Exception as e:
    print(f"[Erro na busca, respondendo offline]: {e}")



# Injetando a pesquisa de atualização na LLM

#concatenando o prompt com a pesquisa na internet
contexto = f"Aqui estão informações atualizadas da internet:\n{resultados}\n\nAgora responda de forma natural à seguinte pergunta do usuário: {prompt}"



mensagens = [
    {
        "role": "system",
        "content": "Você é um robô amigável. Responda sempre usando a informação da internet enviada. Se a informação estiver incompleta ou não tiver a data exata, seja sincero e diga isso de forma simpática. Máximo de 4 frases curtas. IMPORTANTE: É PROIBIDO usar emojis ou caracteres especiais, gere apenas texto puro."
    },
    
    {
        "role": "user", 
        "content": contexto
    }
]


# finalmente, o envio do prompt até a LLM


print("[Sending to Groq...]")


response = client.chat.completions.create(
    model = "qwen/qwen3.8-27b",
    messages = mensagens,
    max_tokens = 999
)

end = time.time()

resposta = response.choices[0].message.content

#tempo de processamento do LLM
print(f"[Groq Processing Time]: {end - start:.2f} seconds")
print(f"\n[Groq Response]: {resposta}")
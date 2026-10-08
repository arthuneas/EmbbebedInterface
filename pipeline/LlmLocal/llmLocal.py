# pyrefly: ignore [missing-import]
import ollama 
import time
import os
# pyrefly: ignore [missing-import]
from ddgs import DDGS

os.system('clear')

prompt = 'me fale sobre deltarune capitulo 5' # usar um texto genérico que a STT transcreve


print("[Searching On Internet...]")
resultados = ""
try: 
    with DDGS() as ddgs:
        # Truque Jedi: Adicionamos o ano atual na busca
        query_busca = prompt + " 2026"
        results = ddgs.text(query_busca, max_results=2)
        for r in results:
            resultados += r['body'] + " "

except Exception as e:
    print(f"[Erro na busca, respondendo offline]: {e}")

start = time.time()

# INJETANDO A PESQUISA NO CÉREBRO DO OLLAMA

contexto = f"Aqui estão informações atualizadas da internet:\n{resultados}\n\nAgora responda de forma natural à seguinte pergunta do usuário: {prompt}"

# aqui adicionamos a personalidade do robô usando o System Prompt
mensagens = [
    
    {
        "role": "system",
        "content": 'Você é um robô amigável. Responda sempre usando a informação da internet enviada. Se a informação estiver incompleta ou não tiver a data exata, seja sincero e diga isso de forma simpática. Máximo de 6 frases curtas. IMPORTANTE: É PROIBIDO usar emojis ou caracteres especiais, gere apenas texto puro.'
    },
    
    {
        'role': 'user',
        'content': contexto,
    },
]


print("[Sending to Local LLM...]\n")

#resposta = ollama.chat(model='llama3.1', messages=mensagens) #mais parâmetros, maior processamento
resposta = ollama.chat(model='gemma2:2b', messages=mensagens) #rapido, mas informações limitadas

end = time.time()

# tempo de execução do LLM
print(f"[LLM Processing Time]: {end - start:.2f} seconds")

# .message.content pega o conteúdo da resposta
print(f"\n[LLM Response]: {resposta['message']['content']}")
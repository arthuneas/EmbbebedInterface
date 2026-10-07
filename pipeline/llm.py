# pyrefly: ignore [missing-import]
import ollama 
import time
import os

os.system('clear')

prompt = 'O que é LLM?' # usar um texto genérico que a STT transcreve

# aqui adicionamos a personalidaded o robô usando o System Prompt
mensagens = [
    
    {
        "role": "system",
        "content": 'Você é um robô educacional super amigável e feliz. Responda a criança se apresentando de volta em no MÁXIMO 2 frases curtas.'
    },
    
    {
        'role': 'user',
        'content': prompt,
    },
]


start = time.time()

print("[Sending to LLM...]\n")

resposta = ollama.chat(model='llama3.2', messages=mensagens)

end = time.time()

# tempo de execução do LLM
print(f"[LLM Processing Time]: {end - start:.2f} seconds")

# .message.content pega o conteúdo da resposta
print(f"\n[LLM Response]: {resposta['message']['content']}")
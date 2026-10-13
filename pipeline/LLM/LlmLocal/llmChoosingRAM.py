# pyrefly: ignore [missing-import]
import ollama
import psutil
import time
import os

def choose_download_model():
    print("\n[MODEL CHOOSING]\n")

    # pega a memória RAM disponivel no sistema em GB
    ram = psutil.virtual_memory().total / (1024 ** 3)

    # escolhe o modelo baseado na RAM disponivel no sistema
    if ram >= 8:
        model = 'llama3.1'

    else: 
        model = 'gemma2:2b'
    
    print(f"[RAM available]: {ram:.2f} GB")
    print(f"[Model choosed]: {model}")

    # verifica se o modelo está baixado no computador
    locals_model = [m['model'] for m in ollama.list()['models']]

    nome = f"{model}:latest"

    if nome not in locals_model and model not in locals_model:
        print(f"\n[Model Not On System]")
        print(f"\n[ Downloading {model}:latest\n")
        
        ollama.pull(model)
        print("\n[Downloaded]\n")

    else:
        print("\n[Model Allready On System]\n")

    return model
    
os.system('clear')


# pede o modelo
model = choose_download_model()

# aqui adicionamos a personalidade do robô usando o System Prompt
prompt = 'Qual o ultimo album da ariana grande?' # usar um texto genérico que a STT transcreve

mensagens = [
    
    {
        "role": "system",
        "content": 'Você é um robô educacional super amigável e feliz. Responda a criança em no máximo 3 frases curtas.'
    },
    
    {
        'role': 'user',
        'content': prompt,
    },
]


start = time.time()

print("[Sending to LLM...]\n")

# Usa a variável 'model' que foi retornada pela nossa função!
resposta = ollama.chat(model=model, messages=mensagens)

end = time.time()

# tempo de execução do LLM
print(f"[LLM Processing Time]: {end - start:.2f} seconds")

# .message.content pega o conteúdo da resposta
print(f"\n[LLM Response]: {resposta['message']['content']}")
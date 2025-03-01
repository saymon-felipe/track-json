import tiktoken
import re
import time
import logging
from openai import OpenAI
from datetime import datetime

# Configuração do cliente OpenAI
client = OpenAI(
    api_key=""
)

# Parâmetros de token e chunk
MAX_TOKENS = 7000  # Limite de tokens do modelo
CHUNK_SIZE = 50    # Tente começar com um valor menor e ajusta conforme necessário

# Configuração do log
def setup_logging():
    # Criando um nome único para o arquivo de log com base na data e hora
    log_filename = f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    
    # Criando o arquivo de log
    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
    )

    # Adicionando também ao console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
    logging.getLogger().addHandler(console_handler)

    logging.info("Início da execução do script")

# Função para contar os tokens em um texto
def count_tokens(text):
    """Conta o número de tokens em um texto usando tiktoken"""
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = len(encoding.encode(text))
    logging.info(f"Contagem de tokens: {tokens} para o texto '{text[:30]}...'")
    print(f"Contagem de tokens: {tokens} para o texto '{text[:30]}...'")  # Exibindo no console
    return tokens

# Função para dividir o texto em pedaços menores
def split_into_chunks(filenames):
    chunks = []
    current_chunk = []
    current_chunk_tokens = 0

    logging.info(f"Iniciando a divisão dos arquivos em chunks...")
    print("Iniciando a divisão dos arquivos em chunks...")  # Exibindo no console
    
    for filename in filenames:
        chunk_text = f"{filename}"
        chunk_tokens = count_tokens(chunk_text)

        # Se adicionar o item ultrapassar o limite de tokens, cria um novo chunk
        if current_chunk_tokens + chunk_tokens > MAX_TOKENS:
            chunks.append(current_chunk)
            logging.info(f"Chunk finalizado com {len(current_chunk)} músicas.")
            print(f"Chunk finalizado com {len(current_chunk)} músicas.")  # Exibindo no console
            current_chunk = [filename]
            current_chunk_tokens = chunk_tokens
        else:
            current_chunk.append(filename)
            current_chunk_tokens += chunk_tokens

    if current_chunk:  # Adiciona o último chunk
        chunks.append(current_chunk)
        logging.info(f"Último chunk adicionado com {len(current_chunk)} músicas.")
        print(f"Último chunk adicionado com {len(current_chunk)} músicas.")  # Exibindo no console
    
    logging.info(f"Divisão completa: {len(chunks)} chunks criados.")
    print(f"Divisão completa: {len(chunks)} chunks criados.")  # Exibindo no console
    return chunks

# Função para formatar os nomes das músicas
def format_song_name(filenames):
    setup_logging()
    chunks = split_into_chunks(filenames)
    formatted_names = []

    processed_files = 0
    
    for i, chunk in enumerate(chunks):
        chunk_text = ", ".join(chunk)
        prompt = f"""
        Os nomes de arquivos que eu vou mandar parecem ser de músicas. 
        Identifique o nome de cada música e o seu respectivo artista com base no nome. 
        Retorne a lista no formato: 1: Artista - Música, 2: Artista - Música, etc".
        
        {chunk_text}
        """
        
        logging.info(f"Enviando o prompt para a OpenAI (Chunk {i + 1}/{len(chunks)}): {chunk_text[:50]}...")
        print(f"Enviando o prompt para a OpenAI (Chunk {i + 1}/{len(chunks)}): {chunk_text[:50]}...")  # Exibindo no console

        try:
            # Solicitação à OpenAI
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )

            formatted_list = response.choices[0].message.content.strip()

            # Verificando se a resposta tem o formato desejado
            if formatted_list:
                logging.info(f"Resposta recebida do GPT-4 para o chunk {i + 1}")
                print(f"Resposta recebida do GPT-4 para o chunk {i + 1}")  # Exibindo no console
                # Extraindo o nome da música formatado
                formatted_names.extend(re.findall(r'\d+: (.+? - .+?)(?=,|$)', formatted_list))
                processed_files += len(formatted_names)

                print(f"🔄 Processadas {processed_files} músicas de {len(filenames)} até agora.")
                logging.info(f"🔄 Processadas {processed_files} músicas de {len(filenames)} até agora.")

                # Escrevendo no log apenas os nomes renomeados
                for name in formatted_names:
                    logging.info(f"Alterado para: {name}")
                    print(f"Alterado para: {name}")  # Exibindo no console
                print(f"✔️ {len(formatted_names)} músicas formatadas e registradas.")
            else:
                logging.error(f"❌ Erro ao formatar os nomes das músicas no chunk {i + 1}. Resposta vazia.")
                print(f"❌ Erro ao formatar os nomes das músicas.")
                return []

        except Exception as e:
            logging.error(f"❌ Erro ao formatar o nome da música no chunk {i + 1}: {e}")
            print(f"❌ Erro ao formatar o nome da música: {e}")
            return []

        # Adicionando um pequeno atraso entre as requisições para evitar bloqueios
        time.sleep(10)

    logging.info(f"Processamento completo. {len(formatted_names)} músicas formatadas.")
    print(f"Processamento completo. {len(formatted_names)} músicas formatadas.")  # Exibindo no console
    return formatted_names
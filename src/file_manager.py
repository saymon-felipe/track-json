import os
import shutil
import re
import time
#from ai_helper import format_song_name  # Importe a função que formata os nomes

def log_message(message, log_file):
    """Registra mensagens no arquivo de log e exibe no console."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  # Obtém a data e hora atual
    log_entry = f"[{timestamp}] {message}\n"
    
    with open(log_file, "a", encoding="utf-8") as log:
        log.write(log_entry)  # Escreve no arquivo de log
    
    print(message)  # Exibe no console também
    
def save_music_titles(folder):
    """Salva todos os nomes das músicas em um único arquivo de texto."""
    music_files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith(('.mp3', '.wav', '.flac'))]
    music_titles = [os.path.splitext(f)[0] for f in music_files]  # Pega apenas o nome, sem a extensão
    
    music_text_folder = os.path.join(folder, "music_text")

    if not os.path.exists(music_text_folder):
        os.makedirs(music_text_folder)

    # Define o caminho do arquivo único
    music_file_path = os.path.join(music_text_folder, "all_music_titles.txt")

    # Salva todos os títulos das músicas em um único arquivo
    with open(music_file_path, 'w', encoding='utf-8') as file:
        file.write("\n".join(music_titles))

    print(f"OK: Arquivo 'all_music_titles.txt' criado com {len(music_titles)} músicas.")
    
def process_music_titles(folder):
    """Lê os títulos das músicas da pasta 'music_text', formata e salva em 'replaced_musics_titles'."""
    
    # Definir caminhos das pastas
    music_text_folder = os.path.join(folder, "music_text")
    replaced_music_folder = os.path.join(folder, "replaced_musics_titles")

    # Garantir que a pasta de saída exista
    if not os.path.exists(replaced_music_folder):
        os.makedirs(replaced_music_folder)

    # Caminho do arquivo de entrada
    input_file = os.path.join(music_text_folder, "all_music_titles.txt")

    # Caminho do arquivo de saída
    output_file = os.path.join(replaced_music_folder, "replaced_music_titles.txt")

    # Verificar se o arquivo de entrada existe
    if not os.path.exists(input_file):
        print(f"ERROR: O arquivo {input_file} não foi encontrado.")
        return
    
    formatted_songs = []

    def format_song_name(song_line):
        song_line = song_line.strip().replace(".", " ")  # Substitui pontos por espaços
        if " - " in song_line:
            parts = song_line.split(" - ", 1)
            artist = parts[0].title().strip()
            song_name = parts[1].title().strip()
            return f"{artist} - {song_name}"
        return song_line.title().strip()

    # Função para limpar o nome da música removendo informações extras
    def clean_song_title(song_title):
        song_title = re.sub(r"\(.*?\)", "", song_title)  # Remover parênteses e conteúdo
        song_title = re.sub(r"\[.*?\]", "", song_title)  # Remover colchetes e conteúdo
        song_title = re.sub(r"\b(\d{2,4}|Ao Vivo|Live|Lançamento|Lanc|Feat|Part|Versão|Acústico)\b", "", song_title, flags=re.IGNORECASE)
        song_title = re.sub(r"\s+", " ", song_title).strip()  # Remover múltiplos espaços
        return song_title

    # Função para corrigir múltiplos separadores "-"
    def fix_extra_hyphens(song):
        parts = song.split(" - ")
        if len(parts) > 2:
            artist = parts[0].strip()
            title = " - ".join(parts[1:]).strip(" -")
            return f"{artist} - {title}"
        return song

    # Ler e processar as músicas do arquivo original
    with open(input_file, "r", encoding="utf-8") as file:
        for line in file:
            formatted_song = format_song_name(line)
            formatted_songs.append(formatted_song)

    # Escrever o novo arquivo formatado
    with open(output_file, "w", encoding="utf-8") as file:
        for song in formatted_songs:
            file.write(song + "\n")

    print(f"OK: Arquivo '{output_file}' criado com {len(formatted_songs)} músicas.")

def rename_files(folder):
    """Renomeia os arquivos de áudio na pasta com base nos nomes dos arquivos de texto e cria cópias na pasta replaced_songs"""
    logs_folder = os.path.join(folder, "logs")  # Criando pasta de logs
    os.makedirs(logs_folder, exist_ok=True)  # Cria a pasta se não existir
    log_file = os.path.join(logs_folder, "rename_files.log")  # Caminho do arquivo de log

    music_text_folder = os.path.join(folder, "replaced_musics_titles")
    replaced_songs_folder = os.path.join(folder, "replaced_songs")

    if not os.path.isdir(music_text_folder):
        log_message(f"ERROR: Pasta 'replaced_musics_titles' não encontrada no caminho: {music_text_folder}", log_file)
        return
    
    os.makedirs(replaced_songs_folder, exist_ok=True)  # Cria a pasta 'replaced_songs' se não existir

    formatted_names = []

    for txt_file in os.listdir(music_text_folder):
        if txt_file.endswith(".txt"):
            txt_file_path = os.path.join(music_text_folder, txt_file)
            
            with open(txt_file_path, 'r', encoding='utf-8') as file:
                content = file.readlines()
                log_message(f"📜 Lendo arquivo: {txt_file} ({len(content)} linhas)", log_file)

                for line in content:
                    line = line.strip()
                    if " - " in line:
                        artist_song = line.split(" - ", 1)
                        formatted_names.append(f"{artist_song[0]} - {artist_song[1]}")

                log_message(f"✅ Nomes formatados extraídos: {formatted_names}", log_file)

    if not formatted_names:
        log_message("ERROR: Nenhum nome de música encontrado nos arquivos de texto.", log_file)
        return

    audio_files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith(('.mp3', '.wav', '.flac'))]

    if len(audio_files) != len(formatted_names):
        log_message(f"WARNING: Atenção! O número de arquivos de áudio ({len(audio_files)}) é diferente do número de músicas no arquivo de texto ({len(formatted_names)}).", log_file)

    for i, audio_file in enumerate(audio_files):
        old_path = os.path.join(folder, audio_file)
        copied_path = os.path.join(replaced_songs_folder, audio_file)  # Copia com o mesmo nome original
        new_name = formatted_names[i] + os.path.splitext(audio_file)[1]  # Novo nome com mesma extensão
        new_path = os.path.join(replaced_songs_folder, new_name)

        try:
            shutil.copy2(old_path, copied_path)  # Copia primeiro
            os.rename(copied_path, new_path)  # Renomeia o arquivo copiado
            log_message(f"OK: Copiado e renomeado: {audio_file} ➡️ {new_name}", log_file)
        except Exception as e:
            log_message(f"ERROR: Erro ao copiar ou renomear {audio_file}: {e}", log_file)

    log_message("OK: Processo de renomeação concluído!", log_file)
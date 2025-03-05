import os
import eyed3
import re

def edit_music_metadata(folder):
    print("LOADING: Editando os metadados da música...")

    # Percorre todos os arquivos na pasta
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)

        # Verifica se é um arquivo de áudio suportado
        if not os.path.isfile(file_path) or not filename.lower().endswith(('.mp3', '.wav', '.flac', '.m4a')):
            continue

        # Tenta capturar o artista e título a partir do nome do arquivo
        match = re.match(r"^(?P<artist>.+?)\s*-\s*(?P<title>.+)$", filename.rsplit('.', 1)[0])
        
        if match:
            # Carrega o arquivo de áudio
            audio_file = eyed3.load(file_path)

            # Verifica se o arquivo foi carregado corretamente
            if audio_file and audio_file.tag:
                # Atualiza as tags
                audio_file.tag.title = match.group('title').strip()
                audio_file.tag.artist = match.group('artist').strip()
                audio_file.tag.save()

                print(f"OK: Arquivo '{filename}' alterado com sucesso.")
            else:
                print(f"ERROR: Não foi possível carregar o arquivo '{filename}' ou ele não possui tags válidas.")
        else:
            print(f"ERROR: O nome do arquivo '{filename}' não segue o padrão 'artista - título'.")

def extract_music_metadata(folder):
    """Extrai metadados de arquivos de áudio e preenche dados ausentes com base no nome do arquivo."""

    music_metadata = []

    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)

        # Verifica se é um arquivo de áudio suportado
        if not os.path.isfile(file_path) or not filename.lower().endswith(('.mp3', '.wav', '.flac', '.m4a')):
            continue

        metadata = {
            "file_name": filename,
            "artist": "Unknown Artist",
            "title": "Unknown Title",
            "album": "Unknown Album",
            "year": None,
            "genre": "Unknown Genre"
        }

        # Tenta carregar os metadados do arquivo de áudio
        if filename.lower().endswith('.mp3'):
            audio_file = eyed3.load(file_path)
            if audio_file and audio_file.tag:
                match = re.match(r"^(?P<artist>.+?)\s*-\s*(?P<title>.+)$", filename.rsplit('.', 1)[0])
                metadata["artist"] = match.group('artist').strip()
                metadata["title"] = match.group('title').strip()
                metadata["album"] = audio_file.tag.album if audio_file.tag.album else metadata["album"]
                metadata["year"] = audio_file.tag.getBestDate().year if audio_file.tag.getBestDate() else metadata["year"]
                metadata["genre"] = audio_file.tag.genre.name if audio_file.tag.genre else metadata["genre"]

        music_metadata.append(metadata)

    return music_metadata

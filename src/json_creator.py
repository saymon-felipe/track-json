import os
import json
from metadata import extract_music_metadata

def generate_json(folder):
    print("INIT: Criando JSON com informações das músicas...")

    # Extrai os metadados de todos os arquivos na pasta
    music_list = extract_music_metadata(folder)

    # Define o diretório de saída na pasta formatted_json
    output_dir = os.path.join(folder, "formatted_json")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "music_data.json")

    # Salva o JSON no diretório
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(music_list, json_file, indent=4, ensure_ascii=False)

    print(f"OK: JSON criado com sucesso: {output_file}")

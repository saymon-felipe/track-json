import os
import time
from file_manager import rename_files, save_music_titles, process_music_titles
from json_creator import generate_json

def loading_animation():
    """Função para simular uma animação de loading simples no terminal"""
    print("LOADING: Ação em progresso", end="")
    for _ in range(3):
        time.sleep(0.5)  # Simula o tempo de processamento
        print(".", end="", flush=True)  # Exibe o ponto de progresso
    print()  # Nova linha após a animação

def main():
    while True:
        print("\n **TrackJSON** ")
        print("1. Criar JSON com informações das músicas")
        print("2. Renomear músicas com nomes padronizados")
        print("3. Sair")
        choice = input("Escolha uma opção: ")

        if choice == "1":
            folder = input("Digite o caminho da pasta com as músicas: ").strip()
            if os.path.isdir(folder):
                print("INIT: Iniciando a criação do JSON...")
                loading_animation()
                generate_json(folder)
                print("OK: JSON criado com sucesso!")
            else:
                print("ERROR: Caminho inválido. Tente novamente.")

        elif choice == "2":
            folder = input("Digite o caminho da pasta com as músicas: ").strip()
            if os.path.isdir(folder):
                print("INIT: Iniciando a renomeação das músicas...")
                loading_animation()
                
                print("LOADING: Extraindo os nomes antigos partir da pasta...")
                loading_animation()
                save_music_titles(folder)
                print("OK: Títulos de músicas extraídos com sucesso!")
                
                loading_animation()
                
                print("LOADING: Criando nomes corretos para as músicas...")
                loading_animation()
                process_music_titles(folder)
                print("OK: Novos nomes criados com sucesso!")
                
                loading_animation()
                
                print("INIT: Renomeando músicas na pasta destino...")
                loading_animation()
                rename_files(folder)
                print("OK: Músicas renomeadas com sucesso!")
            else:
                print("ERROR: Caminho inválido. Tente novamente.")
        elif choice == "3":
            print("END: Saindo do programa. Até mais!")
            time.sleep(3)
            break
        else:
            print("ERROR: Opção inválida. Escolha um número de 1 a 5.")

if __name__ == "__main__":
    main()

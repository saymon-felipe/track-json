# 🎵 TrackJSON

TrackJSON é uma ferramenta simples para organizar arquivos de música, gerando um JSON com informações das faixas e renomeando os arquivos de forma padronizada.

## 🚀 Funcionalidades
- 📦 **Criação de JSON**: Gera um arquivo JSON contendo informações das músicas de uma pasta.
- 📝 **Renomeação de Arquivos**: Renomeia arquivos de música para nomes limpos e padronizados.
- 📝 **Edição de Metadados**: Edita as tags de metadados das músicas com base no nome do arquivo e no artista

## 🛠️ Instalação
1. **Clone o repositório**:
   ```bash
   git clone https://github.com/saymon-felipe/track-json.git
   cd TrackJSON
   ```
2. **Crie um ambiente virtual (opcional, mas recomendado)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate  # Windows
   ```
3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Como Usar
Execute o programa no terminal:
```bash
python main.py
```
Escolha uma opção no menu:
1. Criar JSON com informações das músicas.
2. Renomear músicas com nomes padronizados.
3. Sair do programa.

## 📦 Compilação para Executável
Caso queira transformar o programa em um executável:
```bash
python -m PyInstaller --onefile --clean --icon=icon.ico --name=TrackJSON src/main.py
```
O executável estará disponível na pasta `dist/`.

## 📝 Requisitos
- Python 3.10+
- Bibliotecas: `os`, `time`, `json`, `PIL (Pillow)`

## 📜 Licença
Este projeto está sob a licença MIT. Sinta-se à vontade para modificar e compartilhar! 🎶


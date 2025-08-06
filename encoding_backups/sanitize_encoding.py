import os
import shutil
import chardet
import logging
from pathlib import Path

# --- Configuração ---
PROJECT_PATH = Path.cwd()
BACKUP_DIR = PROJECT_PATH / "encoding_backups"
EXTENSIONS_TO_CHECK = ['.py', '.toml', '.md', '.yml', '.yaml', '.txt', '.json']
# --------------------

logging.basicConfig(level=logging.INFO, format="%(message)s")

def convert_file_to_utf8(file_path: Path):
    """
    Detecta a codificação de um arquivo e o converte para UTF-8 se necessário,
    criando um backup antes da conversão.
    """
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            if not raw_data:
                logging.info(f"[✓] Ignorado (vazio): {file_path.relative_to(PROJECT_PATH)}")
                return

        detected = chardet.detect(raw_data)
        encoding = detected['encoding']

        if encoding and encoding.lower().strip() != 'utf-8':
            logging.warning(f"[!] Detectado '{encoding}' em: {file_path.relative_to(PROJECT_PATH)}")

            # 1. Criar Backup
            relative_path = file_path.relative_to(PROJECT_PATH)
            backup_path = BACKUP_DIR / relative_path
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(file_path, backup_path)
            logging.info(f"    -> Backup criado em: {backup_path.relative_to(PROJECT_PATH)}")

            # 2. Converter e Sobrescrever
            text = raw_data.decode(encoding, errors='replace')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(text)
            logging.info(f"    -> [✔] Convertido com sucesso para UTF-8.")

    except Exception as e:
        logging.error(f"[⚠] Erro ao processar {file_path.relative_to(PROJECT_PATH)}: {e}")

def main():
    """Varre o projeto e executa a conversão."""
    logging.info("--- 🔄 Iniciando Verificação e Conversão de Codificação de Arquivos ---")

    if not BACKUP_DIR.exists():
        BACKUP_DIR.mkdir()
        logging.info(f"Diretório de backup criado em: {BACKUP_DIR.relative_to(PROJECT_PATH)}")

    file_count = 0
    for ext in EXTENSIONS_TO_CHECK:
        for file_path in PROJECT_PATH.rglob(f'*{ext}'):
            if ".venv" not in str(file_path) and "encoding_backups" not in str(file_path):
                convert_file_to_utf8(file_path)
                file_count += 1

    logging.info(f"\n--- ✅ Verificação Concluída. {file_count} arquivos analisados. ---")

if __name__ == "__main__":
    main()

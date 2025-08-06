# start_chroma.py
import os
import subprocess
import sys


def start_chroma_server():
    """Inicia o servidor ChromaDB"""
    print("INFO: Iniciando servidor ChromaDB...")

    # Cria diretório se não existir
    chroma_dir = "./chroma_db"
    if not os.path.exists(chroma_dir):
        os.makedirs(chroma_dir)
        print(f"INFO: Diretório {chroma_dir} criado.")

    try:
        # Inicia o servidor ChromaDB
        cmd = [
            "poetry",
            "run",
            "chroma",
            "run",
            "--path",
            chroma_dir,
            "--host",
            "localhost",
            "--port",
            "8000",
        ]
        print(f"INFO: Executando comando: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"ERRO: Falha ao iniciar ChromaDB: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nINFO: Servidor ChromaDB interrompido pelo usuário.")


if __name__ == "__main__":
    start_chroma_server()

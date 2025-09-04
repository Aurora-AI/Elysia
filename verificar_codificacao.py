import os

import chardet

# Caminho do projeto
caminho_projeto = r"C:\Users\winha\Aurora\Aurora-Plataform"

# Extensões de arquivos que você deseja verificar (adicione mais se necessário)
extensoes_verificadas = [".py", ".txt", ".html", ".js", ".css"]


def verificar_codificacao(caminho_arquivo):
    try:
        with open(caminho_arquivo, "rb") as f:
            resultado = chardet.detect(f.read())
            return resultado["encoding"]
    except Exception as e:
        return f"Erro: {e}"


# Verificação
for raiz, _, arquivos in os.walk(caminho_projeto):
    for arquivo in arquivos:
        if any(arquivo.endswith(ext) for ext in extensoes_verificadas):
            caminho_completo = os.path.join(raiz, arquivo)
            codificacao = verificar_codificacao(caminho_completo)
            if codificacao != "utf-8":
                print(f"[ALERTA] {caminho_completo} está codificado como {codificacao}")

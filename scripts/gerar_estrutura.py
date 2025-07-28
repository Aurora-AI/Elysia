import json
import os


def coletar_estrutura(pasta):
    estrutura = []
    for raiz, dirs, arquivos in os.walk(pasta):
        for arquivo in arquivos:
            caminho = os.path.join(raiz, arquivo)
            tamanho = os.path.getsize(caminho)
            estrutura.append({"nome": arquivo, "caminho": caminho, "tamanho": tamanho})
    return estrutura


with open("estrutura.json", "w", encoding="utf-8") as f:
    json.dump(
        coletar_estrutura(r"C:\Users\winha\Aurora\Aurora-Core"),
        f,
        indent=2,
        ensure_ascii=False,
    )

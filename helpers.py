import os
from jogoteca import app
from config import IMAGEM_PADRAO


def recupera_imagem(jogo):
    nome_da_imagem = f"capa_{jogo.id}_{jogo.nome}"
    result = IMAGEM_PADRAO

    for nome_arquivo in os.listdir(app.config["UPLOAD_PATH"]):
        if nome_da_imagem in nome_arquivo:
            result = nome_arquivo
            break

    return result


def deleta_arquivo(jogo):
    arquivo = recupera_imagem(jogo)

    if arquivo != IMAGEM_PADRAO: 
        os.remove(os.path.join(app.config["UPLOAD_PATH"], arquivo))
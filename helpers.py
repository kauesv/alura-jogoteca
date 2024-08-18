import os
from jogoteca import app
from config import IMAGEM_PADRAO
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, PasswordField


class FormularioJogo(FlaskForm):
    nome = StringField(label='Nome do jogo', validators=[validators.DataRequired(), validators.Length(min=1, max=50)])
    categoria = StringField(label='Categoria', validators=[validators.DataRequired(), validators.Length(min=1, max=40)])
    plataforma = StringField(label='Plataforma', validators=[validators.DataRequired(), validators.Length(min=1, max=20)])

    salvar = SubmitField(label='Salvar')

class FormularioLogin(FlaskForm):
    nickname = StringField(label='Nickname', validators=[validators.DataRequired(), validators.Length(min=1, max=8)])
    senha = PasswordField(label='Senha', validators=[validators.DataRequired(), validators.Length(min=1, max=100)])

    entrar = SubmitField('Entrar')

def recupera_imagem(jogo):
    nome_da_imagem = f"capa_{jogo.id}"
    result = IMAGEM_PADRAO

    for nome_arquivo in os.listdir(app.config["UPLOAD_PATH"]):
        if nome_da_imagem in nome_arquivo:
            result = nome_arquivo
            break

    return result


def deleta_arquivo(jogo):
    arquivo = recupera_imagem(jogo)

    if arquivo != IMAGEM_PADRAO:
        # concatena o diretorio e o arquivo
        os.remove(os.path.join(app.config["UPLOAD_PATH"], arquivo))
from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from models import Jogos, Usuarios
from jogoteca import app, db
import os
from helpers import recupera_imagem, deleta_arquivo
import time


# Primeira rota
@app.route('/', methods=['GET',])
def index():
    return "<h1>Olá Mundo!!</h1>"

#Apresenta um render template
@app.route('/lista', methods=['GET',])
def lista():
    lista_jogos = Jogos.query.order_by(Jogos.id)
    return render_template('lista.html', titulo='Jogos', jogos=lista_jogos)

@app.route("/novo", methods=['GET',])
def novo():
    if ('usuario_logado' not in session) or (session['usuario_logado'] == None):
        
        return redirect(url_for('login', proxima=url_for('novo')))
        #return redirect('/login?proxima=novo')
    return render_template('novo.html', titulo="Novo jogo")

@app.route("/criar", methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    plataforma = request.form['plataforma']

    jogo = Jogos.query.filter_by(nome=nome).first()

    if jogo:
        flash("Jogo já existente!")
        return redirect(url_for('novo'))
    else:
        novo_jogo = Jogos(nome=nome, categoria=categoria, plataforma=plataforma)
        db.session.add(novo_jogo)
        db.session.commit()

        #   Obtem o arquivo e guarda
        arquivo = request.files['arquivo']
        upload_path = app.config["UPLOAD_PATH"]

        #   Resolver o problema de cache do navegador
        # O professor escolheu a opção de colocar timestamp no nome do
        #arquivo para ele ser unico
        timestamp = time.time()

        arquivo.save(f"{upload_path}/capa_{novo_jogo.id}_{nome}-{timestamp}.jpg")

        # Redireciona para a pagina com o nome de função "lista"
        return redirect(url_for('lista'))

#   Obtem o id do lista.html
@app.route("/editar/<int:id>")
def editar(id):
    if ('usuario_logado' not in session) or (session['usuario_logado'] == None):
        return redirect(url_for('login', proxima=url_for('novo')))

    jogo = Jogos.query.filter_by(id=id).first()

    #Obtem imagem
    capa_jogo = recupera_imagem(jogo)

    return render_template('editar.html', titulo="Editando jogo", jogo=jogo, capa_jogo=capa_jogo)

@app.route("/atualizar", methods=['POST',])
def atualizar():
    jogo = Jogos.query.filter_by(id=request.form['id']).first()

    if jogo:
        jogo.nome = request.form['nome']
        jogo.categoria = request.form['categoria']
        jogo.plataforma = request.form['plataforma']
        db.session.add(jogo)
        db.session.commit()

        #   salva alteração do arquivo
        arquivo = request.files['arquivo']
        upload_path = app.config["UPLOAD_PATH"]

        #   Resolver o problema de cache do navegador
        # O professor escolheu a opção de colocar timestamp no nome do
        #arquivo para ele ser unico
        timestamp = time.time()

        #Deleta a imagem anterior
        deleta_arquivo(jogo)

        arquivo.save(f"{upload_path}/capa_{request.form['id']}_{request.form['nome']}-{timestamp}.jpg")

        # Redireciona para a pagina com o nome de função "lista"
        return redirect(url_for('lista'))
    else:
        flash("Jogo Não existente!")
        return redirect(url_for('novo'))

#   Obtem o id do lista.html
@app.route("/deletar/<int:id>")
def deletar(id):
    if ('usuario_logado' not in session) or (session['usuario_logado'] == None):
        return redirect(url_for('login'))

    jogo = Jogos.query.filter_by(id=id).first()
    jogo_id = jogo.id
    jogo_nome = jogo.nome
    Jogos.query.filter_by(id=id).delete()
    db.session.commit()

    upload_path = app.config["UPLOAD_PATH"]
    arquivo = f"{upload_path}/capa_{jogo_id}_{jogo_nome}.jpg"

    # Verifica se o arquivo existe antes de deletar
    if os.path.exists(arquivo):
        os.remove(arquivo)
    else:
        flash(f'{arquivo} não existe.')

    flash(f"Tudo do jogo {jogo_nome} foi deletado com sucesso!!")
    return redirect(url_for('lista'))

@app.route("/login", methods=['GET',])
def login():
    """Renderiza o html de login"""
    proxima = request.args.get('proxima')
    return render_template("login.html", proxima=proxima)


@app.route("/autenticar", methods=['POST',])
def autenticar():
    """"""
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()

    if usuario:
        if request.form['senha'] == usuario.senha:
            #Cook para guardar a sessao do usuario
            session['usuario_logado'] = usuario.nickname

            #permite uma mensagem rapida
            flash(f'{usuario.nickname} logado com sucesso!')

            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
            #return redirect(f'/{proxima_pagina}')
    else:
        #permite uma mensagem rapida
        flash(f'Usuário não logado')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    #Obtem arquivo de um diretorio usando send_from_directory
    return send_from_directory('uploads', nome_arquivo)
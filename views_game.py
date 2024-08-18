from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca import app, db
from models import Jogos
from helpers import recupera_imagem, deleta_arquivo, FormularioJogo
import time
import os


#Apresenta um render template
@app.route('/', methods=['GET',])
def lista():
    lista_jogos = Jogos.query.order_by(Jogos.id)
    return render_template('lista.html', titulo='Jogos', jogos=lista_jogos)

@app.route("/novo", methods=['GET',])
def novo():
    if ('usuario_logado' not in session) or (session['usuario_logado'] == None):
        return redirect(url_for('login', proxima=url_for('novo')))
        #return redirect('/login?proxima=novo')

    form = FormularioJogo()
    return render_template('novo.html', titulo="Novo jogo", form=form)

@app.route("/criar", methods=['POST',])
def criar():
    form = FormularioJogo(request.form)

    #Valida se o form esta certo
    if not form.validate_on_submit():
        return redirect(url_for('novo'))

    nome = form.nome.data
    categoria = form.categoria.data
    plataforma = form.plataforma.data

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

        arquivo.save(f"{upload_path}/capa_{novo_jogo.id}-{timestamp}.jpg")

        # Redireciona para a pagina com o nome de função "lista"
        return redirect(url_for('lista'))

#   Obtem o id do lista.html
@app.route("/editar/<int:id>")
def editar(id):
    if ('usuario_logado' not in session) or (session['usuario_logado'] == None):
        return redirect(url_for('login', proxima=url_for('novo')))

    jogo = Jogos.query.filter_by(id=id).first()

    form = FormularioJogo()
    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.plataforma.data = jogo.plataforma

    #Obtem imagem
    capa_jogo = recupera_imagem(jogo)

    return render_template('editar.html', titulo="Editando jogo", jogo=jogo, capa_jogo=capa_jogo, form=form)

@app.route("/atualizar", methods=['POST',])
def atualizar():
    form = FormularioJogo(request.form)

    #Valida se o form esta certo
    if form.validate_on_submit():
        jogo = Jogos.query.filter_by(id=request.form['id']).first()

        if jogo:
            jogo.nome = form.nome.data
            jogo.categoria = form.categoria.data
            jogo.plataforma = form.plataforma.data
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

            arquivo.save(f"{upload_path}/capa_{request.form['id']}-{timestamp}.jpg")

            # Redireciona para a pagina com o nome de função "lista"
            return redirect(url_for('lista'))
        else:
            flash("Jogo Não existente!")
            return redirect(url_for('novo'))

    return redirect(url_for('lista'))

#   Obtem o id do lista.html
@app.route("/deletar/<int:id>")
def deletar(id):
    if ('usuario_logado' not in session) or (session['usuario_logado'] == None):
        return redirect(url_for('login'))

    jogo = Jogos.query.filter_by(id=id).first()
    jogo_nome = jogo.nome
    deleta_arquivo(jogo)

    Jogos.query.filter_by(id=id).delete()
    db.session.commit()

    flash(f"Tudo do jogo {jogo_nome} foi deletado com sucesso!!")
    return redirect(url_for('lista'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    #Obtem arquivo de um diretorio usando send_from_directory
    return send_from_directory('uploads', nome_arquivo)
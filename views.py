from flask import render_template, request, redirect, session, flash, url_for
from models import Jogos, Usuarios
from jogoteca import app, db


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

        # Redireciona para a pagina com o nome de função "lista"
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

from jogoteca import app
from flask import render_template, request, redirect, session, flash, url_for
from models import Usuarios
from helpers import FormularioLogin
from flask_bcrypt import check_password_hash


@app.route("/login", methods=['GET',])
def login():
    """Renderiza o html de login"""
    form = FormularioLogin()
    proxima = request.args.get('proxima')
    return render_template("login.html", proxima=proxima, form=form)


@app.route("/autenticar", methods=['POST',])
def autenticar():
    """"""
    form = FormularioLogin(request.form)
    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()

    if usuario:
        senha = check_password_hash(pw_hash=usuario.senha, password=form.senha.data)
        if senha:
            #permite uma mensagem rapida
            flash(f'{usuario.nickname} logado com sucesso!')

            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)

    #permite uma mensagem rapida
    flash(f'Usuário ou senha incorreta')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('lista'))
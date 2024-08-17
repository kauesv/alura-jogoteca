from flask import Flask, render_template, request, redirect, session, flash, url_for

class Jogo():
    def __init__(self, nome, categoria, plataforma):
        self._nome=nome
        self._categoria=categoria
        self._plataforma=plataforma
    
    def __str__(self):
        return self._nome


jogo1 = Jogo("God of War", "Aventura", "Console PS2")
jogo2 = Jogo('Skyrim', 'Aventura', 'Console Xbox')
jogo3 = Jogo('Valorant', 'FPS', 'PC')

lista_jogos = [jogo1, jogo2, jogo3]


class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha


usuario1 = Usuario("Bruno Divino", "BD", "alohomora")
usuario2 = Usuario("Camila Ferreira", "Mila", "paozinho")
usuario3 = Usuario("Guilherme Louro", "Cake", "python_eh_vida")

usuarios_nickname = {
    usuario1.nickname :usuario1, 
    usuario2.nickname :usuario2,
    usuario3.nickname :usuario3
}

#Inicializa o Flask
app = Flask(__name__)
#camada de criptografia
app.secret_key = 'Alura'

# Primeira rota
@app.route('/', methods=['GET',])
def index():
    return "<h1>Olá Mundo!!</h1>"

#Apresenta um render template
@app.route('/lista', methods=['GET',])
def lista():
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

    jogo = Jogo(nome, categoria, plataforma)

    lista_jogos.append(jogo)

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
    if request.form['usuario'] in usuarios_nickname:
        usuario = usuarios_nickname[request.form['usuario']]
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


# Roda a aplicação
app.run(debug=True)
#app.run()
#app.run(host='0.0.0.0', port=8080)
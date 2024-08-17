from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy     # pip install flask-sqlalchemy


#Inicializa o Flask
app = Flask(__name__)

#camada de criptografia
app.secret_key = 'Alura'

#conexão com o banco
SGBD = 'mysql+mysqlconnector'
usuario = 'root'
senha = 'admin'
servidor = 'localhost'
database = 'jogoteca'

app.config['SQLALCHEMY_DATABASE_URI'] = f"{SGBD}://{usuario}:{senha}@{servidor}/{database}"

#Instancia o banco de dados do sql alchemy
db = SQLAlchemy(app)

# Criando o model de jogos seguindo como foi criado no banco
class Jogos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(40), nullable=False)
    plataforma = db.Column(db.String(20), nullable=False)

    # tem como foco o usuário final daquela classe já o __repr__
    def __str__(self):
        return self.nome
    
    # tem como objetivo mostrar uma versão em string para a pessoa programadora quando a classe é acessada em modo interativo.
    def __repr__(self):
        return f"<Nome {self.nome}>"


# Criando o model de usuarios seguindo como foi criado no banco
class Usuarios(db.Model):
    nome = db.Column(db.String(20), nullable=False)
    nickname = db.Column(db.String(8), primary_key=True)
    senha = db.Column(db.String(100), nullable=False)

    # tem como foco o usuário final daquela classe já o __repr__
    def __str__(self):
        return self.nome
    
    # tem como objetivo mostrar uma versão em string para a pessoa programadora quando a classe é acessada em modo interativo.
    def __repr__(self):
        return f"<Nome {self.nome}>"


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


# Roda a aplicação
app.run(debug=True)
#app.run()
#app.run(host='0.0.0.0', port=8080)
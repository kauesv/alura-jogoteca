from flask import Flask, render_template


#Inicializa o Flask
app = Flask(__name__)

# Primeira rota
@app.route('/')
def index():
    return "<h1>Olá Mundo!!</h1>"

#Apresenta um render template
@app.route('/jogos')
def lista_jogos():
    return render_template('lista.html')

# Roda a aplicação
app.run()
#app.run(host='0.0.0.0', port=8080)
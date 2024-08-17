from flask_sqlalchemy import SQLAlchemy     # pip install flask-sqlalchemy
from flask import Flask


#   Inicializa o Flask
app = Flask(__name__)

#   Configuração do Banco e camada de criptografia
# a partir do arquivo de config
app.config.from_pyfile('config.py')

#   Instancia o banco de dados do sql alchemy
db = SQLAlchemy(app)

#   Tras todas as rotas
from views import *

#   Garante que rode a aplicação
if __name__ == '__main__':
    #   Roda a aplicação
    app.run(debug=True)
    #app.run()
    #app.run(host='0.0.0.0', port=8080)
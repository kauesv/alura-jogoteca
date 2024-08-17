import os


#camada de criptografia
SECRET_KEY = "Alura"

#conexão com o banco
sgbd = "mysql+mysqlconnector"
usuario = "root"
senha = "admin"
servidor = "localhost"
database = "jogoteca"

SQLALCHEMY_DATABASE_URI = f"{sgbd}://{usuario}:{senha}@{servidor}/{database}"

# dirname retorna o caminho do diretorio config.py
#   __file__ referencia ao arquivo config.py
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + "/uploads"
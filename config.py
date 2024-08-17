#camada de criptografia
SECRET_KEY = 'Alura'

#conexão com o banco
sgbd = 'mysql+mysqlconnector'
usuario = 'root'
senha = 'admin'
servidor = 'localhost'
database = 'jogoteca'

SQLALCHEMY_DATABASE_URI = f"{sgbd}://{usuario}:{senha}@{servidor}/{database}"


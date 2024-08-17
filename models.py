from jogoteca import db


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
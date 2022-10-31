from sqlalchemy import ForeignKey
from easyfit import db

class Musculo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    categoria = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<Name &r>' % self.name

class RelacaoMusculo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ref_1 = db.Column(db.Integer, ForeignKey("musculo.id"))
    ref_2 = db.Column(db.Integer, ForeignKey("musculo.id"), nullable=True)
    ref_3 = db.Column(db.Integer, ForeignKey("musculo.id"), nullable=True)

    def __repr__(self):
        return '<Name &r>' % self.name

class Exercicio(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    relacao_musculo = db.Column(db.Integer, ForeignKey("relacao_musculo.id"))
    descricao = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return '<Name &r>' % self.name

class RelacaoExercicio(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ref_1 = db.Column(db.Integer, ForeignKey("exercicio.id"))
    ref_2 = db.Column(db.Integer, ForeignKey("exercicio.id"), nullable=True)
    ref_3 = db.Column(db.Integer, ForeignKey("exercicio.id"), nullable=True)
    ref_4 = db.Column(db.Integer, ForeignKey("exercicio.id"), nullable=True)
    ref_5 = db.Column(db.Integer, ForeignKey("exercicio.id"), nullable=True)
    ref_6 = db.Column(db.Integer, ForeignKey("exercicio.id"), nullable=True)
    ref_7 = db.Column(db.Integer, ForeignKey("exercicio.id"), nullable=True)
    ref_8 = db.Column(db.Integer, ForeignKey("exercicio.id"), nullable=True)
    ref_9 = db.Column(db.Integer, ForeignKey("exercicio.id"), nullable=True)

    def __repr__(self):
        return '<Name &r>' % self.name

class Treino(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    relacao_musculo = db.Column(db.Integer, ForeignKey("relacao_musculo.id"))
    relacao_exercicio = db.Column(db.Integer, ForeignKey("relacao_exercicio.id"))

    def __repr__(self):
        return '<Name &r>' % self.name

class TreinoCompleto(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    nivel = db.Column(db.String(255), nullable=False)
    objetivo = db.Column(db.String(255), nullable=False)
    foco = db.Column(db.String(255), nullable=False)
    treino_a = db.Column(db.Integer, ForeignKey("treino.id"))
    treino_b = db.Column(db.Integer, ForeignKey("treino.id"), nullable=True)
    treino_c = db.Column(db.Integer, ForeignKey("treino.id"), nullable=True)
    treino_d = db.Column(db.Integer, ForeignKey("treino.id"), nullable=True)
    treino_e = db.Column(db.Integer, ForeignKey("treino.id"), nullable=True)
    treino_f = db.Column(db.Integer, ForeignKey("treino.id"), nullable=True)

    def __repr__(self):
        return '<Name &r>' % self.name

class Usuarios(db.Model):
    nick = db.Column(db.String(8), primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Name &r>' % self.name


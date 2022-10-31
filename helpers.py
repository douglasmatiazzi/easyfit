import os
from easyfit import app
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, PasswordField, SelectField

from models import RelacaoMusculo, RelacaoExercicio, Treino


class FormularioTreinoCompleto(FlaskForm):
    nome = StringField('Nome do Treino', [validators.DataRequired(), validators.Length(min=1, max=255)])
    nivel = SelectField('Nível', choices=['Iniciante', 'Intermediário', 'Avançado'])
    objetivo = SelectField('Objetívo', choices=['Hipertrofia', 'Força', 'Resistência'])
    foco = StringField('Foco', [validators.DataRequired(), validators.Length(min=1, max=255)])
    treino_a = SelectField('treino_a', coerce=int)
    treino_b = SelectField('treino_b', coerce=int)
    treino_c = SelectField('treino_c', coerce=int)
    treino_d = SelectField('treino_d', coerce=int)
    treino_e = SelectField('treino_e', coerce=int)
    treino_f = SelectField('treino_f', coerce=int)
    salvar = SubmitField('Salvar')

def edit_treino_a(request, id):
    treino = Treino.query.get(id)
    form = FormularioTreinoCompleto(request.POST, obj=treino)
    form.treino_a.choices = [(g.id, g.name) for g in Treino.query.order_by('name')]

def edit_treino_b(request, id):
    treino = Treino.query.get(id)
    form = FormularioTreinoCompleto(request.POST, obj=treino)
    form.treino_b.choices = [(g.id, g.name) for g in Treino.query.order_by('name')]

def edit_treino_c(request, id):
    treino = Treino.query.get(id)
    form = FormularioTreinoCompleto(request.POST, obj=treino)
    form.treino_c.choices = [(g.id, g.name) for g in Treino.query.order_by('name')]

def edit_treino_d(request, id):
    treino = Treino.query.get(id)
    form = FormularioTreinoCompleto(request.POST, obj=treino)
    form.treino_d.choices = [(g.id, g.name) for g in Treino.query.order_by('name')]

def edit_treino_e(request, id):
    treino = Treino.query.get(id)
    form = FormularioTreinoCompleto(request.POST, obj=treino)
    form.treino_e.choices = [(g.id, g.name) for g in Treino.query.order_by('name')]

def edit_treino_f(request, id):
    treino = Treino.query.get(id)
    form = FormularioTreinoCompleto(request.POST, obj=treino)
    form.treino_f.choices = [(g.id, g.name) for g in Treino.query.order_by('name')]

class FormularioUsuario(FlaskForm):
    nick = StringField('Nick', [validators.DataRequired(), validators.Length(min=1, max=8)])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1, max=100)])
    login = SubmitField('Login')

def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo
    return 'capa_padrao.jpg'

def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'capa_padrao.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))



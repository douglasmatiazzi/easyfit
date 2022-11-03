import os
from easyfit import app
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, PasswordField, SelectField

from models import RelacaoMusculo, RelacaoExercicio, Treino, Musculo, Exercicio

class FormularioTreinoCompleto(FlaskForm):
    lista_treinos = [(g.id, g.nome) for g in Treino.query.order_by('id')]
    nome = StringField('Nome do Treino', [validators.DataRequired(), validators.Length(min=1, max=255)])
    nivel = SelectField('Nível', choices=['Iniciante', 'Intermediário', 'Avançado'])
    objetivo = SelectField('Objetívo', choices=['Hipertrofia', 'Força', 'Resistência'])
    foco = StringField('Foco', [validators.DataRequired(), validators.Length(min=1, max=255)])
    treino_a = SelectField('treino_a', choices=lista_treinos)
    treino_b = SelectField('treino_b', choices=lista_treinos)
    treino_c = SelectField('treino_c', choices=lista_treinos)
    treino_d = SelectField('treino_d', choices=lista_treinos)
    treino_e = SelectField('treino_e', choices=lista_treinos)
    treino_f = SelectField('treino_f', choices=lista_treinos)
    salvar = SubmitField('Salvar')

class FormularioTreinoDiario(FlaskForm):
    lista_musculos = [(g.id, g.nome) for g in Musculo.query.order_by('id')]
    lista_exercicios = [(g.id, g.nome) for g in Exercicio.query.order_by('id')]
    nome = StringField('Nome do Treino Diário', [validators.DataRequired(), validators.Length(min=1, max=255)])
    musculo_1 = SelectField('musculo_1', choices=lista_musculos)
    musculo_2 = SelectField('musculo_2', choices=lista_musculos)
    musculo_3 = SelectField('musculo_3', choices=lista_musculos)
    exercicio_1 = SelectField('exercício_1', choices=lista_exercicios)
    exercicio_2 = SelectField('exercício_2', choices=lista_exercicios)
    exercicio_3 = SelectField('exercício_3', choices=lista_exercicios)
    exercicio_4 = SelectField('exercício_4', choices=lista_exercicios)
    exercicio_5 = SelectField('exercício_5', choices=lista_exercicios)
    exercicio_6 = SelectField('exercício_6', choices=lista_exercicios)
    exercicio_7 = SelectField('exercício_7', choices=lista_exercicios)
    exercicio_8 = SelectField('exercício_8', choices=lista_exercicios)
    exercicio_9 = SelectField('exercício_9', choices=lista_exercicios)
    salvar = SubmitField('Salvar')

class FormularioExercicio(FlaskForm):
    lista_musculos = [(g.id, g.nome) for g in Musculo.query.order_by('id')]
    lista_exercicios = [(g.id, g.nome) for g in Exercicio.query.order_by('id')]
    nome = StringField('Nome do Exercício', [validators.DataRequired(), validators.Length(min=1, max=255)])
    musculo_1 = SelectField('musculo_1', choices=lista_musculos)
    musculo_2 = SelectField('musculo_2', choices=lista_musculos)
    musculo_3 = SelectField('musculo_3', choices=lista_musculos)
    descricao = StringField('Descrição', [validators.DataRequired(), validators.Length(min=1, max=255)])
    salvar = SubmitField('Salvar')

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



from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from easyfit import app, db
from models import Musculo, RelacaoMusculo, Exercicio, RelacaoExercicio, Treino, TreinoCompleto
from helpers import recupera_imagem, deleta_arquivo, FormularioTreinoCompleto
import time

@app.route('/')
def index():
    lista_treino = TreinoCompleto.query.order_by(TreinoCompleto.id)
    return render_template('lista.html', titulo='Treinos Completos', treinos=lista_treino)


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    form = FormularioTreinoCompleto()
    return render_template('novo.html', titulo='Novo Treino', form=form)


@app.route('/criar', methods=['POST', ])
def criar():
    form = FormularioTreinoCompleto(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novo'))

    nome = form.nome.data
    nivel = form.nivel.data
    objetivo = form.objetivo.data
    foco = form.foco.data
    treino_a = form.treino_a.data
    treino_b = form.treino_b.data
    treino_c = form.treino_c.data
    treino_d = form.treino_d.data
    treino_e = form.treino_e.data
    treino_f = form.treino_f.data
    treino = TreinoCompleto.query.filter_by(nome=nome).first()

    if treino:
        flash('Treino já existente')
        return redirect(url_for('index'))

    novo_treino = TreinoCompleto(nome=nome, nivel=nivel, objetivo=objetivo, foco=foco, treino_a=treino_a,
                                 treino_b=treino_b, treino_c=treino_c, treino_d=treino_d, treino_e=treino_e,
                                 treino_f=treino_f)
    db.session.add(novo_treino)
    db.session.commit()

    arquivo = request.files["arquivo"]
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{novo_treino.id}-{timestamp}.jpg')

    return redirect(url_for('index'))


@app.route('/treino/<int:id>')
def treino(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('treino', id=id)))

    treino = Treino.query.filter_by(id=id).first()

    rel_musculo = RelacaoMusculo.query.filter_by(id=treino.relacao_musculo).first()
    musculo_1 = Musculo.query.filter_by(id=rel_musculo.ref_1).first()
    musculo_2 = Musculo.query.filter_by(id=rel_musculo.ref_2).first()
    musculo_3 = Musculo.query.filter_by(id=rel_musculo.ref_3).first()
    musculos = [musculo_1, musculo_2, musculo_3]

    rel_exercicio = RelacaoExercicio.query.filter_by(id=treino.relacao_exercicio).first()
    exercicio_1 = Exercicio.query.filter_by(id=rel_exercicio.ref_1).first()
    exercicio_2 = Exercicio.query.filter_by(id=rel_exercicio.ref_2).first()
    exercicio_3 = Exercicio.query.filter_by(id=rel_exercicio.ref_3).first()
    exercicio_4 = Exercicio.query.filter_by(id=rel_exercicio.ref_4).first()
    exercicio_5 = Exercicio.query.filter_by(id=rel_exercicio.ref_5).first()
    exercicio_6 = Exercicio.query.filter_by(id=rel_exercicio.ref_6).first()
    exercicio_7 = Exercicio.query.filter_by(id=rel_exercicio.ref_7).first()
    exercicio_8 = Exercicio.query.filter_by(id=rel_exercicio.ref_8).first()
    exercicio_9 = Exercicio.query.filter_by(id=rel_exercicio.ref_9).first()
    exercicios = [exercicio_1, exercicio_2, exercicio_3, exercicio_4, exercicio_5, exercicio_6, exercicio_7, exercicio_8, exercicio_9]

    treino_musculos_exercicios = [treino, musculos, exercicios]

    return render_template('treino.html', titulo='Treino', id=id, treino_musculos_exercicios=treino_musculos_exercicios)

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))
    treino = TreinoCompleto.query.filter_by(id=id).first()
    form = FormularioTreinoCompleto()
    form.nome.data = treino.nome
    form.nivel.data = treino.nivel
    form.objetivo.data = treino.objetivo
    form.treino_a.data = treino.treino_a
    form.treino_b.data = treino.treino_b
    form.treino_c.data = treino.treino_c
    form.treino_d.data = treino.treino_d
    form.treino_e.data = treino.treino_e
    form.treino_f.data = treino.treino_f
    capa_treino = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando Treino', id=id, capa_treino=capa_treino, form=form)


@app.route('/atualizar', methods=['POST', ])
def atualizar():
    form = FormularioTreinoCompleto(request.form)
    if form.validate_on_submit():
        treino = TreinoCompleto.query.filter_by(id=request.form['id']).first()
        nome = form.nome.data
        nivel = form.nivel.data
        objetivo = form.objetivo.data
        foco = form.foco.data
        treino_a = form.treino_a.data
        treino_b = form.treino_b.data
        treino_c = form.treino_c.data
        treino_d = form.treino_d.data
        treino_e = form.treino_e.data
        treino_f = form.treino_f.data

        db.session.add(treino)
        db.session.commit()

        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        deleta_arquivo(id)
        arquivo.save(f'{upload_path}/capa{treino.id}-{timestamp}.jpg')

    return redirect(url_for('index'))


@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    TreinoCompleto.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Treino deletado com sucesso')
    return redirect(url_for('index'))


@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

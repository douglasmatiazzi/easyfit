from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from easyfit import app, db
from models import Musculo, RelacaoMusculo, Exercicio, RelacaoExercicio, Treino, TreinoCompleto
from helpers import recupera_imagem, deleta_arquivo, FormularioTreinoCompleto, FormularioTreinoDiario, \
                    FormularioExercicio
import time

@app.route('/')
def index():
    lista_treino = TreinoCompleto.query.order_by(TreinoCompleto.id)
    return render_template('lista.html', titulo='Treinos Completos', treinos=lista_treino)


@app.route('/novo_treino_completo')
def novo_treino_completo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo_treino_completo')))
    form = FormularioTreinoCompleto()
    return render_template('novo_treino_completo.html', titulo='Novo Treino', form=form)

@app.route('/novo_treino_diario')
def novo_treino_diario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo_treino_diario')))
    form = FormularioTreinoDiario()
    return render_template('novo_treino_diario.html', titulo='Novo Treino Diário', form=form)

@app.route('/novo_exercicio')
def novo_exercicio():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo_exercicio')))
    form = FormularioExercicio()
    return render_template('novo_exercicio.html', titulo='Novo Exercício', form=form)

@app.route('/criar', methods=['POST', ])
def criar():
    form = FormularioTreinoCompleto(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novo_treino_completo'))

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

@app.route('/criar_treino_diario', methods=['POST', ])
def criar_treino_diario():
    form = FormularioTreinoDiario(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novo_treino_diario'))

    nome = form.nome.data
    musculo_1 = form.musculo_1.data
    musculo_2 = form.musculo_2.data
    musculo_3 = form.musculo_3.data
    exercicio_1 = form.exercicio_1.data
    exercicio_2 = form.exercicio_2.data
    exercicio_3 = form.exercicio_3.data
    exercicio_4 = form.exercicio_4.data
    exercicio_5 = form.exercicio_5.data
    exercicio_6 = form.exercicio_6.data
    exercicio_7 = form.exercicio_7.data
    exercicio_8 = form.exercicio_8.data
    exercicio_9 = form.exercicio_9.data
    treino = Treino.query.filter_by(nome=nome).first()

    if treino:
        flash('Treino Diário já existente')
        return redirect(url_for('index'))

    nova_relacao_musculo = RelacaoMusculo(ref_1=musculo_1, ref_2=musculo_2, ref_3=musculo_3)
    nova_relacao_exercicio = RelacaoExercicio(ref_1=exercicio_1, ref_2=exercicio_2, ref_3=exercicio_3,
                                              ref_4=exercicio_4, ref_5=exercicio_5, ref_6=exercicio_6,
                                              ref_7=exercicio_7, ref_8=exercicio_8, ref_9=exercicio_9)

    db.session.add(nova_relacao_musculo, nova_relacao_exercicio)
    db.session.commit()

    nova_relacao_musculo = RelacaoMusculo.query.filter_by(ref_1=musculo_1, ref_2=musculo_2, ref_3=musculo_3).first()
    nova_relacao_exercicio = RelacaoExercicio.query.filter_by(ref_1=exercicio_1, ref_2=exercicio_2, ref_3=exercicio_3,
                                                              ref_4=exercicio_4, ref_5=exercicio_5, ref_6=exercicio_6,
                                                              ref_7=exercicio_7, ref_8=exercicio_8, ref_9=exercicio_9).first()
    novo_treino_diario = Treino(nome=nome, relacao_musculo=nova_relacao_musculo.id,
                                relacao_exercicio=nova_relacao_exercicio.id)
    db.session.add(novo_treino_diario)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/criar_exercicio', methods=['POST', ])
def criar_exercicio():
    form = FormularioExercicio(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novo_exercicio'))

    nome = form.nome.data
    descricao = form.descricao.data
    exercicio = Exercicio.query.filter_by(nome=nome).first()

    if exercicio:
        flash('Exercício já existente')
        return redirect(url_for('index'))

    musculo_1 = form.musculo_1.data
    musculo_2 = form.musculo_2.data
    musculo_3 = form.musculo_3.data

    nova_relacao_musculo = RelacaoMusculo(ref_1=musculo_1, ref_2=musculo_2, ref_3=musculo_3)
    db.session.add(nova_relacao_musculo)
    db.session.commit()

    nova_relacao_musculo = RelacaoMusculo.query.filter_by(ref_1=musculo_1, ref_2=musculo_2, ref_3=musculo_3).first()
    novo_exercicio = Exercicio(nome=nome, relacao_musculo=nova_relacao_musculo.id,
                                descricao=descricao)
    db.session.add(novo_exercicio)
    db.session.commit()
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

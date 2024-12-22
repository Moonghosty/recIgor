from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort, make_response
from models.viagem import Viagem, lista_viagens

loginController = Blueprint('login', __name__)

@loginController.route("/")
def inicial():
    return render_template("index.html")

def inicializar_sessao():
    if 'viagens' not in session:
        session['viagens'] = []
def obter_total_viagens():
    total_viagens = request.cookies.get('totalViagens')
    return int(total_viagens) if total_viagens else 0

@loginController.route('/')
def listar_viagens():
    inicializar_sessao()
    if not session['viagens']:
        return redirect(url_for('index', 500))

    viagens = session['viagens']
    total_viagens = obter_total_viagens()
    return render_template('index.html', viagens=viagens, total_viagens=total_viagens)

@loginController.route('/index', methods=['GET', 'POST'])
def cadastro_viagem():
    if request.method == 'POST':
        lugar = request.form.get('lugar')
        data = request.form.get('data')
        descricao = request.form.get('descricao')
        nota = request.form.get('nota')

        if not lugar or not data or not descricao or not nota or int(nota) not in range(1, 6):
            return redirect(url_for('index', 500))

        nova_viagem = Viagem(lugar, data, descricao, nota)
        session['viagens'].append(nova_viagem)

        total_viagens = obter_total_viagens() + 1
        resp = make_response(redirect(url_for('listar_viagens')))
        resp.set_cookie('totalViagens', str(total_viagens), max_age=86400)
        return resp

    error = request.args.get('error')
    return render_template('cadastro.html', error=error)

@loginController.route('/limpar', methods=['POST'])
def limpar_diario():
    session.pop('viagens', None)
    resp = make_response(redirect(url_for('listar_viagens')))
    resp.delete_cookie('totalViagens')
    return resp
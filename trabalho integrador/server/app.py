from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime, timedelta
from banco_de_dados import BancoDeDados
from functools import wraps

#const
TIMEOUT = 600 #segundos

dir = 'client/templates'
app = Flask(__name__, template_folder=dir)
banco = BancoDeDados()

app.secret_key = 'chave'  # não faço a minima para que isso serve, mas se tirar dá erro
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(seconds=TIMEOUT)

@app.before_request
def before_request():
    session.permanent = True  #adiciona tempo de vida a sessão
#funcoes
def popout():
    session.pop('usuario', None)
    return True

#decoradores
def is_autenticado(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function



@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'usuario' in session:
        session.pop('usuario', None)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        resultadoS = banco.validar_senha(password, username)
        if resultadoS == 'senha':
            flash('Senha incorreta!')
        elif resultadoS == 'usuario':
            flash('Usuário não encontrado!')
        else:
            session['usuario'] = resultadoS
            tempo = TIMEOUT
            return redirect(url_for('menu'))

    return render_template('login.html')

@app.route('/menu')
@is_autenticado
def menu():
    return render_template('menu.html')

@app.route('/buscar', methods=['GET', 'POST'])
@is_autenticado
def buscar():
    if request.method == 'POST':
        id_c = request.form['id']
        nome = request.form['nome']
        cpf = request.form['cpf']
        senha = request.form['senha']
        resultadoS = banco.validar_senha(senha, session['usuario'])
        if resultadoS == 'senha':
            flash('Senha incorreta!')
            return render_template('buscar.html')
        elif resultadoS == 'usuario':
            flash('Usuário não encontrado!')
            return render_template('buscar.html')
        else:
            resultado = banco.buscar_registro_cliente(id_c, nome, cpf)
            return render_template('resultado.html', resultado=resultado)
    return render_template('buscar.html')

@app.route('/buscarusuario', methods=['GET', 'POST'])
@is_autenticado
def buscarusuario():
    if request.method == 'POST':
        id_u = request.form['id']
        usuario = request.form['usuario']
        resultado = banco.buscar_registro_usuario(id_u, usuario)
        return render_template('resultadousuario.html', resultado=resultado)
    return render_template('buscarusuario.html')

@app.route('/adicionar', methods=['GET', 'POST'])
@is_autenticado
def adicionar():
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        historico = request.form['historico']
        score = request.form['score']
        banco.adicionar_registro_cliente(nome, cpf, historico, score)
        return redirect(url_for('menu'))
    return render_template('adicionar.html')

@app.route('/adicionarusuario', methods=['GET', 'POST'])
@is_autenticado
def adicionarusuario():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        per = int(request.form['per'])
        banco.adicionar_registro_usuario(usuario, senha, per)
        return redirect(url_for('menu'))
    return render_template('adicionarusuario.html')

@app.route('/atualizar/<int:id>', methods=['GET', 'POST'])
@is_autenticado
def atualizar(id):
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        historico = request.form['historico']
        score = request.form['score']
        banco.atualizar_registro_cliente(id, nome, cpf, historico, score)
        return redirect(url_for('menu'))
    resultados = banco.buscar_registro_cliente(id, "", "")[0]
    return render_template('atualizar.html', resultados=resultados)

@app.route('/atualizarusuario/<int:id>', methods=['GET', 'POST'])
@is_autenticado
def atualizarusuario(id):
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        per = request.form['per']
        if id == 1:
            return "Não é possível alterar o usuário admin!"
        banco.atualizar_registro_usuario(id, usuario, senha, per)
        return redirect(url_for('menu'))
    resultados = banco.buscar_registro_usuario(id, "")[0]
    return render_template('atualizarusuario.html', resultados=resultados)

@app.route('/deletar/<int:id>', methods=['GET'])
@is_autenticado
def deletar(id):
    banco.excluir_registro(1, id)
    return redirect(url_for('menu'))

@app.route('/deletarusuario/<int:id>', methods=['GET'])
@is_autenticado
def deletarusuario(id):
    if id != 1:
        banco.excluir_registro(2, id)
    return redirect(url_for('menu'))

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if tempo == 0:
    session.pop('usuario', None)

if __name__ == '__main__':
    app.run(debug=True)

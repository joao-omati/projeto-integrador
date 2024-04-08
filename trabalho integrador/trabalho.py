from flask import Flask, render_template, request, redirect, url_for, session
from banco_de_dados import BancoDeDados
from functools import wraps

app = Flask(__name__)
banco = BancoDeDados()
app.secret_key = 'chavesupersecreta'  # não faço a minima para que isso serve, mas se tirar dá erro


def is_autenticado():
    if 'usuario' not in session:
        return False
    return True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'usuario' in session:
        session.pop('usuario', None)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        result = banco.validar_senha(password, username)
        if result == 'senha':
            return "Senha incorreta!"
        elif result == 'usuario':
            return "Usuário inválido!"
        else:
            session['usuario'] = result
            return redirect(url_for('menu'))

    return render_template('login.html')


@app.route('/menu')
def menu():
    if is_autenticado():
        return render_template('menu.html')
    else:
        return redirect(url_for('login'))


@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    if is_autenticado():
        if request.method == 'POST':
            id_c = request.form['id']
            nome = request.form['nome']
            cpf = request.form['cpf']
            print(id_c, nome, cpf)
            resultado = banco.buscar_registro_cliente(id_c, nome, cpf)
            return render_template('resultado.html', resultado=resultado)
        return render_template('buscar.html')
    else:
        return redirect(url_for('login'))


@app.route('/buscarusuario', methods=['GET', 'POST'])
def buscarusuario():
    if is_autenticado():
        if request.method == 'POST':
            id_u = request.form['id']
            usuario = request.form['usuario']
            resultado = banco.buscar_registro_usuario(id_u, usuario)
            return render_template('resultado.html', resultado=resultado)
        return render_template('buscarusuario.html')
    else:
        return redirect(url_for('login'))


@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if is_autenticado():
        if request.method == 'POST':
            nome = request.form['nome']
            cpf = request.form['cpf']
            historico = request.form['historico']
            score = request.form['score']
            banco.adicionar_registro_cliente(nome, cpf, historico, score)
            return redirect(url_for('menu'))
        return render_template('adicionar.html')
    else:
        return redirect(url_for('login'))


@app.route('/adicionarusuario', methods=['GET', 'POST'])
def adicionarusuario():
    if is_autenticado():
        if request.method == 'POST':
            usuario = request.form['usuario']
            senha = request.form['senha']
            per = int(request.form['per'])
            banco.adicionar_registro_usuario(usuario, senha, per)
            return redirect(url_for('menu'))
        return render_template('adicionar.html')
    else:

        return redirect(url_for('login'))





@app.route('/atualizar/<int:id>', methods=['GET', 'POST'])
def atualizar(id):
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        historico = request.form['historico']
        score = request.form['score']
        banco.atualizar_registro_cliente(id, nome, cpf, historico, score)
        return redirect(url_for('menu'))
    if is_autenticado():
        print(id)
        resultados = banco.buscar_registro_cliente(id, "", "")[0]

        return render_template('atualizar.html', resultados=resultados)
    else:
        return redirect(url_for('login'))


@app.route('/excluir', methods=['GET', 'POST'])
def excluir():
    if is_autenticado():
        if request.method == 'POST':
            tipo = int(request.form['tipo'])
            cid = int(request.form['cid'])
            banco.excluir_registro(tipo, cid, None)
            return redirect(url_for('menu'))
        return render_template('excluir.html')
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)

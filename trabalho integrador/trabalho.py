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
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if banco.validar_senha(password, username) == 'senha':
            return "Senha incorreta!"
        elif banco.validar_senha(password, username) == 'usuario':
            return "Usuário inválido!"
        else:
            session['usuario'] = banco.validar_senha(password, username)
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
            tipo = int(request.form['tipo'])
            resultado = banco.buscar_registro(tipo, None, None)
            return render_template('resultado.html', resultado=resultado)
        return render_template('buscar.html')
    else:
        return redirect(url_for('login'))


@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if is_autenticado():
        if request.method == 'POST':
            tipo = int(request.form['tipo'])
            banco.adicionar_registro(tipo, None)
            return redirect(url_for('menu'))
        return render_template('adicionar.html')
    else:
        return redirect(url_for('login'))


@app.route('/atualizar', methods=['GET', 'POST'])
def atualizar():
    if is_autenticado():
        if request.method == 'POST':
            tipo = int(request.form['tipo'])
            cid = int(request.form['cid'])
            resultado = banco.buscar_registro(tipo, None, None)
            banco.atualizar_registro(resultado[cid], None, tipo)
            return redirect(url_for('menu'))
        return render_template('atualizar.html')
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

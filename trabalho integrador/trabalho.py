from flask import Flask, render_template, request, redirect, url_for
from banco_de_dados import BancoDeDados

app = Flask(__name__)
banco = BancoDeDados()

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
            return redirect(url_for('menu'))
    return render_template('login.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    if request.method == 'POST':
        tipo = int(request.form['tipo'])
        resultado = banco.buscar_registro(tipo, None, None)
        return render_template('resultado.html', resultado=resultado)
    return render_template('buscar.html')

@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        tipo = int(request.form['tipo'])
        banco.adicionar_registro(tipo, None)
        return redirect(url_for('menu'))
    return render_template('adicionar.html')

@app.route('/atualizar', methods=['GET', 'POST'])
def atualizar():
    if request.method == 'POST':
        tipo = int(request.form['tipo'])
        cid = int(request.form['cid'])
        resultado = banco.buscar_registro(tipo, None, None)
        banco.atualizar_registro(resultado[cid], None, tipo)
        return redirect(url_for('menu'))
    return render_template('atualizar.html')

@app.route('/excluir', methods=['GET', 'POST'])
def excluir():
    if request.method == 'POST':
        tipo = int(request.form['tipo'])
        cid = int(request.form['cid'])
        banco.excluir_registro(tipo, cid, None)
        return redirect(url_for('menu'))
    return render_template('excluir.html')

@app.route('/logout')
def logout():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
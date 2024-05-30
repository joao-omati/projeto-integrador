from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime, timedelta
from banco_de_dados import BancoDeDados
from functools import wraps
#const
EXPTIME = 2

#caso queira mudar o diretorio de templates
#dir = 'local das templates'
#app = Flask(__name__, template_folder=dir)

app = Flask(__name__)
banco = BancoDeDados()

app.secret_key = 'secrKy23'
app.permanent_session_lifetime = timedelta(minutes=EXPTIME)


def popout():
    session.pop('usuario', None)
    session.pop('ult_alt', None)
    return True

#decoradores
def is_autenticado(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorador



@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if 'usuario' in session:
      popout()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        resultadoS = banco.validar_senha(password, username)
        if resultadoS == 'senha':
            flash('Senha incorreta!')
        elif resultadoS == 'usuario':
            flash('Usuário não encontrado!')
        else:
            print("login realizado")
            session['usuario'] = resultadoS
            session.permanent = True
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
        senhaCad = request.form['senhaCad']
        per = int(request.form['per'])
        senha = request.form['senha']
        res = banco.validar_senha(senha, session['usuario'][1])
        if res != "usuario" and res != "senha":

            banco.adicionar_registro_usuario(usuario, senhaCad, per)
            return redirect(url_for('menu'))
        else:
            return redirect(url_for("adicionarusuario", message=res))
    return render_template('adicionarusuario.html')

@app.route('/atualizar/<int:id>', methods=['GET', 'POST'])
@is_autenticado
def atualizar(id):
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        historico = request.form['historico']
        score = request.form['score']
        senha = request.form['senha']

        res = banco.validar_senha(senha, session['usuario'][1])
        print(res,type(res))
        if res != "usuario" and res != "senha":
                print("b")
                banco.atualizar_registro_cliente(id, nome, cpf, historico, score)
                return redirect(url_for('menu'))
        else:
            print("a")
            return redirect(url_for("atualizar", id=id, message=res))
    resultados = banco.buscar_registro_cliente(id, "", "")[0]
    return render_template('atualizar.html', resultados=resultados)

@app.route('/atualizarusuario/<int:id>', methods=['GET', 'POST'])
@is_autenticado
def atualizarusuario(id):
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senhaCad']
        per = request.form['per']
        senha = request.form['senha']
        
        res = banco.validar_senha(senha, session['usuario'][1])
        if res != "usuario" and res != "senha":
            if id == 1:
                return redirect(url_for("atualizarusuario", id=id, message="Não é possível alterar o usuário admin!"))
            banco.atualizar_registro_usuario(id, usuario, senha, per)
            return redirect(url_for('menu'))
    resultados = banco.buscar_registro_usuario(id, "")[0]
    return render_template('atualizarusuario.html', resultados=resultados)

""" @app.route('/deletar/<int:id>', methods=['POST'])
@is_autenticado
def deletar(id):
    if request.method == 'POST':
        senha = request.form['delete-senha']
        print(senha)   
        res = banco.validar_senha(senha, session['usuario'][1])
        if res != "usuario" and res != "senha":
            banco.excluir_registro(1, id)
            return redirect(url_for('menu'))
        else:
            return redirect(url_for("atualizar", id=id, message=res))
    return redirect(url_for('menu')) """

@app.route('/deletar/<int:id>', methods=['GET', 'POST'])
@is_autenticado
def deletar(id):
    if request.method == 'POST':
        senha = request.form['senha']
        print(senha)
        res = banco.validar_senha(senha, session['usuario'][1])
        print(res)
        if res != "usuario" and res != "senha":
            banco.excluir_registro(1, id)
            return redirect(url_for('menu'))
        else:
            return redirect(url_for("atualizar", id=id, message=res))
    return redirect(url_for('menu'))

@app.route('/deletarusuario/<int:id>', methods=['GET', 'POST'])
@is_autenticado
def deletarusuario(id):
    if id != 1:
        if request.method == 'POST':
            senha = request.form['senha']
            print(senha)
            res = banco.validar_senha(senha, session['usuario'][1])
            print(res)
            if res != "usuario" and res != "senha":
                banco.excluir_registro(2, id)
                return redirect(url_for('menu'))
            else:
                return redirect(url_for("atualizarusuario", id=id, message=res))
        return redirect(url_for('menu'))
    else:
        return redirect(url_for("atualizarusuario", id=id, message="Não é possível deletar o usuário admin!"))
    
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)

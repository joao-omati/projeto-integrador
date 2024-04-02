import sqlite3
import bcrypt


# todo Tem muitos metodos, com muito overlap entre metodos na tabela cliente com tabela usuarios, otimizar isso!


def hashar_senhas(senha):
    senha = senha.encode('utf-8')
    sal = bcrypt.gensalt(10)
    senha_hash = bcrypt.hashpw(senha, sal)
    return senha_hash


class BancoDeDados:
    def __init__(self, nome_banco="banco.db"):  # deixei assim caso precise mudar o nome do banco
        self.con = sqlite3.connect(nome_banco)
        self.cursor = self.con.cursor()
        # checa se as table existem, e cria se nao existirem
        busca_res = self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        if busca_res.fetchone() is None:
            self.criar_banco()

    def login(self):  # todo Remover, somente usada na versão de console, usar validar_senha pra versao web
        while True:
            usuario_input = input("Usuario, Identifique-se: ")
            senha_input = input("Senha: ")
            resultado = self.validar_senha(senha_input, usuario_input)
            if resultado == "senha":
                print("Senha incorreta!\n")
            elif resultado == "usuario":
                print("Usuario invalido!\n")
            else:
                busca_res = self.cursor.execute('SELECT * FROM usuario WHERE usuario_usuario LIKE ?', (usuario_input,))
                dados = busca_res.fetchone()
                input(f"Bem vindo de volta {dados[1]}, Aperte ENTER para continuar...")
                return dados

    def validar_senha(self, senha_input, usuario):
        busca_res = self.cursor.execute('SELECT * FROM usuario WHERE usuario_usuario LIKE ?', (usuario,))
        dados = busca_res.fetchone()
        if dados is None:
            return "usuario"
        else:
            senha = senha_input.encode("utf-8")
            if bcrypt.checkpw(senha, dados[2]):
                return dados[0]
            else:
                return "senha"

    def confirmar_alteracao(self, usuario):
        while True:  # todo mudar esse loop
            senha_input = input("Digite sua senha, ou aperte 0 para retornar: ")
            if senha_input == "0":
                return 0
            resultado = self.validar_senha(senha_input, usuario)
            if resultado == "senha":
                print("Senha incorreta!\n")
            elif resultado == "usuario":
                print("Usuario invalido!\n")
            else:
                return 1

    def criar_banco(self):
        self.cursor.execute("""
            CREATE TABLE "cliente" (
                "cliente_id"	INTEGER,
                "cliente_nome"	TEXT,
                "cliente_cpf"	TEXT,
                "cliente_historico"	TEXT,
                "cliente_score"	INTEGER,
                PRIMARY KEY("cliente_id" AUTOINCREMENT)
            );

        """)
        self.con.commit()
        self.cursor.execute("""
            CREATE TABLE "usuario" (
                "usuario_id"	INTEGER,
                "usuario_usuario"	TEXT UNIQUE,
                "usuario_senha"	TEXT,
                "usuario_nivel"	INTEGER,
                PRIMARY KEY("usuario_id" AUTOINCREMENT)
            );

        """)
        self.con.commit()
        senha = hashar_senhas(input("Digite senha para o usuario admin: "))
        self.cursor.execute(
            'INSERT INTO usuario (usuario_usuario, usuario_senha, usuario_nivel) VALUES (?, ?, ?)',
            ("admin", senha, 3))

        self.con.commit()

    def buscar_registro(self, tipo, usuario_senha, usario_nome):
        if tipo == 1:  # todo consertar
            dado_busca = input("Insira nome ou CPF para busca, ou * para exibir todos: ")
        elif tipo == 2:
            dado_busca = input("Insira Usuario para busca, ou * para exibir todos: ")

        if dado_busca != "*":
            if tipo == 1:
                table, coluna = "cliente", "cliente_nome"
            elif tipo == 2:
                self.confirmar_alteracao(usuario_senha)
                table, coluna = "usuario", "usuario_usuario"
            if dado_busca.isdigit() and tipo == 1:
                busca_res = self.cursor.execute('SELECT * FROM cliente WHERE cliente_cpf LIKE ?', (f'%{dado_busca}%',))
            else:
                busca_res = self.cursor.execute(f'SELECT * FROM {table} WHERE {coluna} LIKE ?', (f'%{dado_busca}%',))
        else:
            if tipo == 1:
                table = "cliente"
            elif tipo == 2:
                self.confirmar_alteracao(usario_nome)
                table = "usuario"
            busca_res = self.cursor.execute(f'SELECT * FROM {table}')
        return busca_res.fetchall()

    def adicionar_registro(self, tipo, usuario_nome):
        if self.confirmar_alteracao(usuario_nome) == 1:
            if tipo == 1:
                nome = input("Insira nome: ")
                cpf = input("Insira CPF: ")
                historico = input("Insira historico de pagamento em dia separado por vírgula: ")
                score = int(input("Insira Score: "))
                self.cursor.execute(
                    'INSERT INTO cliente (cliente_nome, cliente_cpf, cliente_historico, cliente_score) VALUES '
                    '(?, ?, ?, ?)',
                    (nome, cpf, historico, score))
            elif tipo == 2:
                usuario = input("Insira o Usuário: ")
                senha = hashar_senhas(input("Insira a senha: "))
                per = int(input("Insira o nível de permissão (1 - Usuário, 2 - Supervisor): "))
                self.cursor.execute(
                    'INSERT INTO usuario (usuario_usuario, usuario_senha, usuario_nivel) VALUES (?, ?, ?)',
                    (usuario, senha, per))

            self.con.commit()
            input("Adicionado com sucesso! Aperte ENTER para prosseguir")

    def atualizar_registro(self, resultado, usuario_nome, tipo):
        if self.confirmar_alteracao(usuario_nome) == 1:
            if tipo == 1:
                nova = ["", input("Insira novo nome ou aperte ENTER para pular essa entrada: "),
                        input("Insira novo CPF ou aperte ENTER para pular essa entrada: "),
                        input("Insira novo Histórico de pagamentos em dia ou aperte ENTER para pular essa entrada: "),
                        input("Insira novo Score ou aperte ENTER para pular essa entrada: ")]
                for i in range(1, len(nova)):
                    if nova[i] != "":
                        resultado[i] = nova[i]
                self.cursor.execute(
                    'UPDATE cliente SET cliente_nome = ?, cliente_cpf = ?, cliente_historico = ?, cliente_score = ? '
                    'WHERE cliente_id = ?',
                    (resultado[1], resultado[2], resultado[3], resultado[4], resultado[0]))
            elif tipo == 2:
                nova = ["", input("Insira novo usuário ou aperte ENTER para pular essa entrada: "),
                        hashar_senhas(input("Insira nova senha ou aperte ENTER para pular essa entrada: ")),
                        int(input("Insira novo nível de permissão de pagamentos em dia ou aperte ENTER para pular essa "
                                  "entrada: "))]
                for i in range(1, len(nova)):
                    if nova[i] != "":
                        resultado[i] = nova[i]
                self.cursor.execute(
                    'UPDATE usuario SET usuario_usuario = ?, usuario_senha = ?, usuario_nivel = ? WHERE '
                    'usuario_id = ?',
                    (resultado[1], resultado[2], resultado[3], resultado[0]))
            self.con.commit()
            input("Atualizado com sucesso! Aperte ENTER para prosseguir")

        else:
            return

    def excluir_registro(self, tipo, cid, usuario_nome):        

        if tipo == 1:
            tipo = "cliente"
        elif tipo == 2:
            tipo = "usuario"
        if self.confirmar_alteracao(usuario_nome) == 1:
            self.cursor.execute(f'DELETE FROM {tipo} WHERE {tipo}_id = ?;', cid)
            self.con.commit()
            input("Excluido com sucesso! Aperte ENTER para prosseguir.")
        else:
            return

    def fechar_conexao(self):
        self.con.close()
        print("Conexão fechada com sucesso!")
import sqlite3
from faker import Faker
import string
import random as r
import bcrypt
#Esse codigo inteiro é mal feito e ineficiente, mas é somente usado para teste
fake = Faker('pt_BR')
dados = []

meta = int(input("Criar quantos registros?"))
if int(input("Tipo de registro do banco: 1 = Cliente, 2 = Usuario")) == 1:
    for Y in range(meta):

        nomes_completos = fake.name()
        cpfs = fake.cpf().translate(str.maketrans('', '', string.punctuation))
        score = r.randint(1, 1000)
        historico = set()
        for x in range(25):
            ano = str(r.randint(1990, 2024))
            historico.add(ano)
        historico = list(sorted(historico))  # todo melhorar esas converção, esta indo de set > list > string
        historico = ','.join(historico)
        per = r.randint(1, 2)

        dados.append((nomes_completos, cpfs, score, historico))

    con = sqlite3.connect("banco.db")
    cur = con.cursor()

    for item in dados:
        print("Nome completo:", item[0])
        print("CPF:", item[1])
        print("Score:", item[2])
        print("Historico de pagamentos em dia:", item[3])

        cur.execute("""
            INSERT INTO cliente (cliente_nome, cliente_cpf, cliente_historico, cliente_score) VALUES (?, ?, ?, ?)
        """, (item[0], item[1], item[3], item[2]))
        con.commit()
else:

    for Y in range(meta):
        usuario = fake.user_name()
        senha = fake.password()
        per = r.randint(1,2)
        dados.append((usuario, senha, per))
    con = sqlite3.connect("banco.db")
    cur = con.cursor()
    for item in dados:
        print("Usuario:", item[0])
        print("Senha:", item[1])
        senha = item[1].encode('utf-8')
        salt = bcrypt.gensalt(10)
        senha = bcrypt.hashpw(senha, salt)
        print("Senha HASH:", senha)
        print("Permissao:", item[2])
        cur.execute("""
            INSERT INTO usuario (usuario_usuario, usuario_senha, usuario_nivel) VALUES (?, ?, ?)
        """, (item[0], senha, item[2]))
        con.commit()
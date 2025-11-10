import sqlite3
from db import conectar, criar_tabela

# Criar a tabela na primeira execução
criar_tabela()

def inserir_usuario(nome, email, idade):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nome, email, idade) VALUES (?, ?, ?)", (nome, email, idade))
    conn.commit()
    conn.close()

def listar_usuarios():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    for linha in cursor.fetchall():
        print(linha)
    conn.close()

def buscar_usuario(nome):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE nome LIKE ?", ('%' + nome + '%',))
    for linha in cursor.fetchall():
        print(linha)
    conn.close()

def atualizar_usuario(id, novo_nome, novo_email, nova_idade):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE usuarios
        SET nome = ?, email = ?, idade = ?
        WHERE id = ?
    """, (novo_nome, novo_email, nova_idade, id))
    conn.commit()
    conn.close()

def deletar_usuario(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (id,))
    conn.commit()
    conn.close()

while True:
    print("\n=== SISTEMA DE USUÁRIOS ===")
    print("1. Inserir usuário")
    print("2. Listar usuários")
    print("3. Buscar usuário")
    print("4. Atualizar usuário")
    print("5. Deletar usuário")
    print("0. Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == '1':
        nome = input("Nome: ")
        email = input("Email: ")
        idade = int(input("Idade: "))
        inserir_usuario(nome, email, idade)
        print("Usuário cadastrado com sucesso!")

    elif opcao == '2':
        listar_usuarios()

    elif opcao == '3':
        nome = input("Digite o nome para buscar: ")
        buscar_usuario(nome)

    elif opcao == '4':
        id = int(input("ID do usuário a atualizar: "))
        novo_nome = input("Novo nome: ")
        novo_email = input("Novo email: ")
        nova_idade = int(input("Nova idade: "))
        atualizar_usuario(id, novo_nome, novo_email, nova_idade)
        print("Usuário atualizado!")

    elif opcao == '5':
        id = int(input("ID do usuário a deletar: "))
        deletar_usuario(id)
        print("Usuário removido!")

    elif opcao == '0':
        print("Saindo...")
        break
    else:
        print("Opção inválida!")

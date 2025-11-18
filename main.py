import sqlite3
from db import conectar, criar_tabela

# Biblioteca para cores no terminal
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    print("⚠️ Instale o colorama com: pip install colorama")
    exit()

# Cria a tabela (somente na primeira execução)
criar_tabela()

# ----------------- Funções CRUD -----------------

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
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def buscar_usuario(nome):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE nome LIKE ?", ('%' + nome + '%',))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

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

# ----------------- Validações -----------------

def validar_nome(nome: str) -> bool:
    for c in nome:
        if not (c.isalpha() or c.isspace()):
            return False
    return len(nome.strip()) > 0

def validar_idade(idade: str) -> bool:
    return idade.isdigit() and 1 <= len(idade) <= 2

def validar_email(email: str) -> bool:
    if "@" not in email:
        return False
    parte_usuario, _, parte_dominio = email.partition("@")
    if "." not in parte_dominio or not parte_usuario or not parte_dominio.split(".")[-1]:
        return False
    return True

# ---------------- MENU TERMINAL ----------------

if __name__ == "__main__":
    while True:
        print(Fore.MAGENTA + "\n=== SISTEMA DE USUÁRIOS ===")
        print("1. Inserir usuário")
        print("2. Listar usuários")
        print("3. Buscar usuário")
        print("4. Atualizar usuário")
        print("5. Deletar usuário")
        print("0. Sair")

        opcao = input(Fore.YELLOW + "Escolha uma opção: ")

        if opcao == '1':
            nome = input("Nome: ").strip()
            if not validar_nome(nome):
                print(Fore.RED + "❌ O nome deve conter apenas letras e espaços.")
                continue

            email = input("Email: ").strip()
            if not validar_email(email):
                print(Fore.RED + "❌ Email inválido.")
                continue

            idade = input("Idade: ").strip()
            if not validar_idade(idade):
                print(Fore.RED + "❌ Idade deve ter 1 a 2 números.")
                continue

            inserir_usuario(nome, email, int(idade))
            print(Fore.GREEN + "Usuário cadastrado!")

        elif opcao == '2':
            dados = listar_usuarios()
            if not dados:
                print(Fore.YELLOW + "Nenhum usuário encontrado.")
            else:
                for d in dados:
                    print(Fore.CYAN + str(d))

        elif opcao == '3':
            nome = input("Nome para buscar: ")
            dados = buscar_usuario(nome)
            if not dados:
                print(Fore.YELLOW + "Nenhum encontrado.")
            else:
                for d in dados:
                    print(Fore.CYAN + str(d))

        elif opcao == '4':
            id = int(input("ID: "))
            novo_nome = input("Nome: ")
            novo_email = input("Email: ")
            nova_idade = input("Idade: ")

            if not validar_nome(novo_nome) or not validar_email(novo_email) or not validar_idade(nova_idade):
                print(Fore.RED + "❌ Dados inválidos.")
                continue

            atualizar_usuario(id, novo_nome, novo_email, int(nova_idade))
            print(Fore.GREEN + "Atualizado!")

        elif opcao == '5':
            id = int(input("ID: "))
            deletar_usuario(id)
            print(Fore.GREEN + "Removido!")

        elif opcao == '0':
            print("Saindo...")
            break

        else:
            print("Opção inválida.")

import sqlite3

# Conectar ao banco (cria se não existir)
def conectar():
    return sqlite3.connect("database.sqlite")

# Criar tabela
def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            idade INTEGER
        )
    """)
    conn.commit()
    conn.close()

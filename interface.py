import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from db import conectar
import main  # usa suas funções e validações

# ------------ Funções ------------

def cadastrar():
    nome = nome_entry.get().strip()
    email = email_entry.get().strip()
    idade = idade_entry.get().strip()

    if not main.validar_nome(nome):
        messagebox.showerror("Erro", "Nome inválido! Use apenas letras.")
        return

    if not main.validar_email(email):
        messagebox.showerror("Erro", "Email inválido!")
        return

    if not main.validar_idade(idade):
        messagebox.showerror("Erro", "Idade inválida! Use até 2 dígitos.")
        return

    main.inserir_usuario(nome, email, int(idade))
    messagebox.showinfo("Sucesso", "Usuário cadastrado!")
    limpar_campos()
    listar_usuarios()

def listar_usuarios():
    lista.delete(*lista.get_children())
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    dados = cursor.fetchall()
    conn.close()

    for row in dados:
        lista.insert("", "end", values=row)

def carregar_dados(event):
    item = lista.focus()
    if not item:
        return

    valores = lista.item(item, "values")

    id_var.set(valores[0])
    nome_entry.delete(0, tk.END)
    nome_entry.insert(0, valores[1])

    email_entry.delete(0, tk.END)
    email_entry.insert(0, valores[2])

    idade_entry.delete(0, tk.END)
    idade_entry.insert(0, valores[3])

def atualizar():
    user_id = id_var.get()
    if not user_id:
        messagebox.showwarning("Atenção", "Selecione um usuário na tabela.")
        return

    nome = nome_entry.get().strip()
    email = email_entry.get().strip()
    idade = idade_entry.get().strip()

    if not main.validar_nome(nome):
        messagebox.showerror("Erro", "Nome inválido!")
        return

    if not main.validar_email(email):
        messagebox.showerror("Erro", "Email inválido!")
        return

    if not main.validar_idade(idade):
        messagebox.showerror("Erro", "Idade inválida!")
        return

    main.atualizar_usuario(int(user_id), nome, email, int(idade))
    messagebox.showinfo("Sucesso", "Cadastro atualizado!")
    
    listar_usuarios()
    limpar_campos()

def deletar():
    item = lista.focus()
    if not item:
        messagebox.showwarning("Aviso", "Selecione um usuário.")
        return

    valores = lista.item(item, "values")
    user_id = valores[0]

    confirm = messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este usuário?")
    if not confirm:
        return

    main.deletar_usuario(user_id)
    messagebox.showinfo("Removido", "Usuário deletado!")
    
    listar_usuarios()
    limpar_campos()

def limpar_campos():
    id_var.set("")
    nome_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    idade_entry.delete(0, tk.END)

# ------------ Interface ------------

root = tb.Window(themename="superhero")
root.title("Sistema de Usuários")
root.geometry("600x550")

tb.Label(root, text="Cadastro / Atualização", font=("Segoe UI", 14, "bold")).pack(pady=10)

# Variável oculta para armazenar ID do usuário selecionado
id_var = tk.StringVar()

frm = tb.Frame(root)
frm.pack(pady=10)

tb.Label(frm, text="Nome:", font=("Segoe UI", 12)).grid(row=0, column=0, sticky="w")
nome_entry = tb.Entry(frm, width=40)
nome_entry.grid(row=0, column=1, pady=5)

tb.Label(frm, text="Email:", font=("Segoe UI", 12)).grid(row=1, column=0, sticky="w")
email_entry = tb.Entry(frm, width=40)
email_entry.grid(row=1, column=1, pady=5)

tb.Label(frm, text="Idade:", font=("Segoe UI", 12)).grid(row=2, column=0, sticky="w")
idade_entry = tb.Entry(frm, width=40)
idade_entry.grid(row=2, column=1, pady=5)

tb.Button(frm, text="Cadastrar Novo", bootstyle=SUCCESS, command=cadastrar).grid(row=3, column=1, sticky="w", pady=10)
tb.Button(frm, text="Atualizar Cadastro", bootstyle=PRIMARY, command=atualizar).grid(row=3, column=1, sticky="e", pady=10)

# --- TABELA ---
tb.Label(root, text="Usuários Cadastrados", font=("Segoe UI", 12, "bold")).pack()

cols = ("ID", "Nome", "Email", "Idade")
lista = tb.Treeview(root, columns=cols, show="headings", height=10, bootstyle=INFO)
lista.pack(fill="both", expand=True, pady=10)

for col in cols:
    lista.heading(col, text=col)
    lista.column(col, width=140)

lista.bind("<<TreeviewSelect>>", carregar_dados)

# Botão excluir
tb.Button(root, text="Excluir Selecionado", bootstyle=DANGER, command=deletar).pack(pady=5)

listar_usuarios()

root.mainloop()

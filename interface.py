import tkinter as tk
from tkinter import ttk, messagebox
import sistema




def tela_login():
    login = tk.Tk()
    login.title("Login")
    tk.Label(login, text="Bem-vindo ao Sistema de Cadastro", font=("Arial", 14)).pack(pady=10)
    largura_janela = 400
    altura_janela = 400

    largura_tela = login.winfo_screenwidth()
    altura_tela = login.winfo_screenheight()

    pos_x = (largura_tela // 2) - (largura_janela // 2)
    pos_y = (altura_tela // 2) - (altura_janela // 2)

    login.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")




    tk.Label(login, text="CPF").pack()
    cpf_entry = tk.Entry(login)
    cpf_entry.pack()

    tk.Label(login, text="Senha").pack()
    senha_entry = tk.Entry(login, show="*")
    senha_entry.pack()

    def autenticar():
        cpf = cpf_entry.get()
        senha = senha_entry.get()
        usuario = sistema.autenticar_usuario(cpf, senha)
        if usuario:
            login.destroy()
            tela_principal()
        else:
            messagebox.showerror("Erro", "CPF ou senha inválidos")

    def registrar():
        login.destroy()
        tela_registro()

    tk.Button(login, text="Entrar", command=autenticar).pack(pady=5)
    tk.Button(login, text="Registrar", command=registrar).pack()
    login.mainloop()

def tela_registro():
    reg = tk.Tk()
    reg.title("Registro")
    reg.geometry("300x350")

    tk.Label(reg, text="Nome").pack()
    nome_entry = tk.Entry(reg)
    nome_entry.pack()

    tk.Label(reg, text="Email").pack()
    email_entry = tk.Entry(reg)
    email_entry.pack()

    tk.Label(reg, text="Data de Nascimento").pack()
    data_nascimento_entry = tk.Entry(reg)
    data_nascimento_entry.pack()

    tk.Label(reg, text="CPF").pack()
    cpf_entry = tk.Entry(reg)
    cpf_entry.pack()

    tk.Label(reg, text="Senha").pack()
    senha_entry = tk.Entry(reg, show="*")
    senha_entry.pack()

    def registrar():
        nome = nome_entry.get()
        email = email_entry.get()
        data_nascimento = int(data_nascimento.entry.get())
        cpf = cpf_entry.get()
        senha = senha_entry.get()
        if sistema.registrar_usuario(nome, email, data_nascimento, cpf, senha):
            messagebox.showinfo("Sucesso", "Usuário registrado com sucesso!")
            reg.destroy()
            tela_login()
        else:
            messagebox.showerror("Erro", "CPF já registrado.")

    tk.Button(reg, text="Registrar", command=registrar).pack(pady=10)
    reg.mainloop()

def tela_principal():
    root = tk.Tk()
    root.title("Sistema de Cadastro")
    root.geometry("700x500")

    tree = ttk.Treeview(root, columns=("ID", "Nome", "Email", "Data de Nascimento", "CPF"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
    tree.pack(fill=tk.BOTH, expand=True)

    def atualizar_lista():
        for row in tree.get_children():
            tree.delete(row)
        for usuario in sistema.buscar_usuarios():
            tree.insert("", tk.END, values=usuario)

    def buscar():
        termo = busca_entry.get()
        resultados = sistema.buscar_por_nome_ou_cpf(termo)
        for row in tree.get_children():
            tree.delete(row)
        for usuario in resultados:
            tree.insert("", tk.END, values=usuario)

    def exportar():
        sistema.exportar_csv()
        messagebox.showinfo("Exportação", "Dados exportados para CSV.")

    def sair():
        root.destroy()
        tela_login()

    busca_entry = tk.Entry(root)
    busca_entry.pack()
    tk.Button(root, text="Buscar", command=buscar).pack()

    tk.Button(root, text="Exportar CSV", command=exportar).pack(pady=5)
    tk.Button(root, text="Sair para Login", command=sair).pack(pady=5)

    atualizar_lista()
    root.mainloop()


tela_login()

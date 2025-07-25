import sqlite3
import hashlib
import csv

DB_NAME = "usuarios.db"

def conectar():
    return sqlite3.connect(DB_NAME)

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def registrar_usuario(nome, email, data_nascimento, cpf, senha):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (nome, email, data_nascimento, cpf, senha) VALUES (?, ?, ?, ?, ?)",
                       (nome, email, data_nascimento, cpf, hash_senha(senha)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def autenticar_usuario(cpf, senha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE cpf = ? AND senha = ?", (cpf, hash_senha(senha)))
    usuario = cursor.fetchone()
    conn.close()
    return usuario

def buscar_usuarios():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, email, data_nascimento, cpf FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

def buscar_por_nome_ou_cpf(termo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, email, data_nascimento, cpf FROM usuarios WHERE nome LIKE ? OR cpf LIKE ?", 
                   (f"%{termo}%", f"%{termo}%"))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def editar_usuario(id, nome, email, data_nascimento, cpf):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET nome = ?, email = ?, data_nascimento = ?, cpf = ? WHERE id = ?",
                   (nome, email, data_nascimento, cpf, id))
    conn.commit()
    conn.close()

def excluir_usuario(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def exportar_csv(nome_arquivo="usuarios_exportados.csv"):
    usuarios = buscar_usuarios()
    with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Nome", "Email", "Data de Nascimento", "CPF"])
        writer.writerows(usuarios)

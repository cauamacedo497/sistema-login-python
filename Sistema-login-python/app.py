from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "segredo123"

def conectar():
    return sqlite3.connect("banco.db")

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.route("/cadastrar", methods=["POST"])
def cadastrar():

    nome = request.form["nome"]
    email = request.form["email"]
    senha = generate_password_hash(request.form["senha"])

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO usuarios (nome,email,senha) VALUES (?,?,?)",
        (nome,email,senha)
    )

    conn.commit()

    return redirect("/")

@app.route("/entrar", methods=["POST"])
def entrar():

    email = request.form["email"]
    senha = request.form["senha"]

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM usuarios WHERE email=?",
        (email,)
    )

    usuario = cursor.fetchone()

    if usuario and check_password_hash(usuario[3], senha):
        session["usuario"] = usuario[1]
        return redirect("/dashboard")
    else:
        return "Login inválido"

@app.route("/dashboard")
def dashboard():

    if "usuario" in session:
        return render_template("dashboard.html", nome=session["usuario"])
    else:
        return redirect("/")

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect("/")

@app.route("/criar_banco")
def criar():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        email TEXT,
        senha TEXT
    )
    """)

    conn.commit()

    return "Banco criado!"

app.run(debug=True)
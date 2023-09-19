from flask import Flask, render_template, request, redirect, flash
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = "palavra-secreta123"

@app.route("/")
def home():
    return render_template('/login.html')

@app.route("/login", methods=['POST'])
def login():
    usuario = request.form.get("username")
    senha = request.form.get("password")
    with open('data/usuarios.json') as usuarios:
        lista = json.load(usuarios)
        for c in lista:
            if usuario == c['username'] and senha == c['password']:
                return render_template("/index.html", nomeUsuario=c['username'])
        flash('Usuário Inválido')
    return redirect("/")

@app.route("/logout")
def logout():
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)

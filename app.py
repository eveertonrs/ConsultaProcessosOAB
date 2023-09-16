from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Dicionário para armazenar os usuários (apenas para fins de teste)
users = {'teste': 'teste'}

@app.route('/')
def root():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verifique se o usuário e a senha correspondem aos registros de teste
        if username in users and users[username] == password:
            # Se a autenticação for bem-sucedida, redirecione o usuário para a página inicial
            return redirect('/home')
        else:
            # Se a autenticação falhar, exiba uma mensagem de erro
            error_message = "Usuário ou senha incorretos. Tente novamente."
            return render_template('login.html', error=error_message)
    
    # Se for um pedido GET, apenas renderize a página de login
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

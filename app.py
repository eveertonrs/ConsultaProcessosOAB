from flask import Flask, render_template

# Crie uma instância do aplicativo Flask
app = Flask(__name__)

# Crie uma rota para a página inicial
@app.route('/')
def home():
    return render_template('index.html')

# Execute o aplicativo Flask
if __name__ == '__main__':
    app.run(debug=True)


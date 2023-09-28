from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify
from selenium import webdriver
import time
import socket
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from flask import Flask, render_template, request, redirect, flash, session
from threading import Thread
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager 
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = "palavra-secreta123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc:///?odbc_connect=DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=DB_ConsultaOAB;UID=master;PWD=****'
db = SQLAlchemy(app)

listainf = []
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False) 


def scrape_data():
   # Configurar o serviço do Chrome para rodar em segundo plano
    chrome_service = Service(ChromeDriverManager().install())

    # Configurar as opções do Chrome para o modo headless
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')  # Desativar a aceleração de GPU, às vezes é necessário

    # Inicialize o driver do Chrome com as opções configuradas
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)


        
    driver.get('https://esaj.tjsp.jus.br/cpopg/open.do')
    time.sleep(5)

    elemento_select = driver.find_element(By.ID, 'cbPesquisa')
    select = Select(elemento_select)

    # Selecione a opção com o value igual a "NUMOAB"
    select.select_by_value('NUMOAB')
    campo = driver.find_element(By.ID, 'campo_NUMOAB')
    campo.send_keys('485605')

    btnConsultar = driver.find_element(By.ID, 'botaoConsultarProcessos')

    btnConsultar.click()

    time.sleep(5)

    # Localize a div principal que contém todos os elementos de processo
    div_processos = driver.find_element(By.ID, 'listagemDeProcessos')

    # Localize todos os elementos de processo (li) dentro da div principal
    elementos_processo = div_processos.find_elements(By.TAG_NAME, 'li')
    # Crie uma lista vazia para armazenar os links dos processos
    links_processos = []
    

    # Itere sobre os elementos de processo e extraia os links
    for elemento in elementos_processo:
        link_processo = elemento.find_element(By.TAG_NAME, 'a').get_attribute('href')
        links_processos.append(link_processo)
        print(links_processos)

    # Agora você tem uma lista de links dos processos
    # Itere sobre esses links e acesse cada página de detalhes do processo
    for link_processo in links_processos:
        driver.get(link_processo)
            
        # Encontre e extraia as informações da página de detalhes do processo
        numero_processo = driver.find_element(By.ID, 'numeroProcesso').text
        classe_processo = driver.find_element(By.ID, 'classeProcesso').text
        assunto_processo = driver.find_element(By.ID, 'assuntoProcesso').text
        foro_processo = driver.find_element(By.ID, 'foroProcesso').text
        vara_processo = driver.find_element(By.ID, 'varaProcesso').text
        juiz_processo = driver.find_element(By.ID, 'juizProcesso').text

        # Imprima as informações
        print(f'Número do Processo: {numero_processo}')
        print(f'Classe do Processo: {classe_processo}')
        print(f'Assunto do Processo: {assunto_processo}')
        print(f'Foro do Processo: {foro_processo}')
        print(f'Vara do Processo: {vara_processo}')
        print(f'Juiz do Processo: {juiz_processo}')
        
        # Encontre e extraia as informações da movimentação na mesma página
        elementos_movimentacao = driver.find_elements(By.CLASS_NAME, 'containerMovimentacao')

        # Defina o número de primeiras movimentações que você deseja coletar
        numero_de_movimentacoes = 5  # Altere para o número desejado
        
        movimentacoes = []

        # Itere sobre as primeiras movimentações
        for elemento in elementos_movimentacao[:numero_de_movimentacoes]:
            # Encontre os elementos dentro de <tr> que contêm as informações
            data_movimentacao = elemento.find_element(By.CLASS_NAME, 'dataMovimentacao').text
            descricao_movimentacao = elemento.find_element(By.CLASS_NAME, 'descricaoMovimentacao').text
            
            movimentacoes.append({
            "data_movimentacao": data_movimentacao,
            "descricao_movimentacao": descricao_movimentacao
            })

            # Imprima as informações da movimentação
            print(f'Data de Movimentação: {data_movimentacao}\n')
            print(f'Descrição da Movimentação: {descricao_movimentacao}\n')
            
        listainf.append({
            "numero_processo": numero_processo,
            "classe_processo": classe_processo,
            "assunto_processo": assunto_processo,
            "foro_processo": foro_processo,
            "vara_processo": vara_processo,
            "juiz_processo": juiz_processo,
            "movimentacoes": movimentacoes
        })

        driver.back()
        
           
    print(listainf)

    # Encerre o driver do Chrome
    driver.quit()


@app.route("/")
def home():
    if listainf:
        return render_template('/index.html', nomeUsuario=session['username'], scraped_data=listainf)
    else:
        return render_template('/login.html')

@app.route("/login", methods=['POST'])
def login():
    usuario = request.form.get("username")
    senha = request.form.get("password")
    
    user = Usuario.query.filter_by(username=usuario).first()
    
    if user and user.password == senha:
        # Store the username in the session variable
        session['username'] = user.username
        scrape_data()
        
        return redirect("/")
    else:
        flash('Usuário ou senha inválidos')
        return redirect("/")

@app.route("/logout")
def logout():
    # Clear the session variables
    session.clear()
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)

from selenium import webdriver
import time
import socket
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Configurar o serviço do Chrome para rodar em segundo plano
chrome_service = Service(ChromeDriverManager().install())

# Configurar as opções do Chrome para o modo headless
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')  # Desativar a aceleração de GPU, às vezes é necessário

# Inicialize o driver do Chrome com as opções configuradas
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)


# # Configure o caminho absoluto para o executável do ChromeDriver
# caminho_para_o_executável_do_chromedriver = r'C:\Projeto trabalhos\ConsultarProcessosOAB\chromedriver.exe'
# # Inicialize o driver do Chrome
# driver = webdriver.Chrome()

# Agora você pode usar o objeto 'driver' para automatizar o Google Chrome
# Por exemplo, navegar para uma página da web:
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

# Variável para armazenar as informações
# informacoes_processos = []

# print("TODOS OS PROCESSOS")
# # Itere sobre os elementos de processo e colete as informações
# for elemento in elementos_processo:
#     numero_processo = elemento.find_element(By.CLASS_NAME, 'nuProcesso').text.strip()
#     advogado = elemento.find_element(By.CLASS_NAME, 'nomeParte').text.strip()
#     classe_processo = elemento.find_element(By.CLASS_NAME, 'classeProcesso').text.strip()
#     assunto_principal = elemento.find_element(By.CLASS_NAME, 'assuntoPrincipalProcesso').text.strip()
#     recebido_em = elemento.find_element(By.CLASS_NAME, 'dataLocalDistribuicaoProcesso').text.strip()

#     informacoes_processos.append(f"{numero_processo}\nAdvogado(a):\n{advogado}\n{classe_processo}\n{assunto_principal}\nRecebido em:\n{recebido_em}\n")

# # Imprima as informações coletadas no formato desejado
# for info in informacoes_processos:
#     print(info)
#     print()

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

    # Itere sobre as primeiras movimentações
    for elemento in elementos_movimentacao[:numero_de_movimentacoes]:
        # Encontre os elementos dentro de <tr> que contêm as informações
        data_movimentacao = elemento.find_element(By.CLASS_NAME, 'dataMovimentacao').text
        descricao_movimentacao = elemento.find_element(By.CLASS_NAME, 'descricaoMovimentacao').text

        # Imprima as informações da movimentação
        print(f'Data de Movimentação: {data_movimentacao}\n')
        print(f'Descrição da Movimentação: {descricao_movimentacao}\n')

    driver.back()

driver.quit()
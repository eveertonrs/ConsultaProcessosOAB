from selenium import webdriver
import time
import socket
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By  # Importe a classe By

# Configure o caminho absoluto para o executável do ChromeDriver
caminho_para_o_executável_do_chromedriver = r'C:\Projeto trabalhos\ConsultarProcessosOAB\chromedriver.exe'

# Inicialize o driver do Chrome
driver = webdriver.Chrome()

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

# Obtém todos os links para os detalhes dos processos
links_processos = driver.find_elements(By.XPATH, '//a[contains(@href, "/cpopg/show.do?processo.numero=")]')
links_processos = [link.get_attribute('href') for link in links_processos]

# Agora você tem uma lista de links para os detalhes de cada processo
# Itere sobre esses links e colete as informações detalhadas
informacoes_processos = []

for link_processo in links_processos:
    driver.get(link_processo)
    informacoes = {}
    
    try:
        # Coleta as informações disponíveis na página de detalhes do processo
        numero_processo = driver.find_element(By.ID, 'numeroProcesso').text
        classe_processo = driver.find_element(By.ID, 'classeProcesso').text
        assunto_processo = driver.find_element(By.ID, 'assuntoProcesso').text
        foro_processo = driver.find_element(By.ID, 'foroProcesso').text
        vara_processo = driver.find_element(By.ID, 'varaProcesso').text
        juiz_processo = driver.find_element(By.ID, 'juizProcesso').text

        informacoes['Número do Processo'] = numero_processo
        informacoes['Classe do Processo'] = classe_processo
        informacoes['Assunto do Processo'] = assunto_processo
        informacoes['Foro do Processo'] = foro_processo
        informacoes['Vara do Processo'] = vara_processo
        informacoes['Juiz do Processo'] = juiz_processo
    except:
        pass
    
    try:
        # Coleta informações de movimentações, se disponíveis
        movimentacoes = driver.find_elements(By.XPATH, '//div[@class="containerMovimentacao"]')
        informacoes['Movimentações'] = []

        for movimentacao in movimentacoes[:5]:  # Coleta apenas as 5 primeiras movimentações
            data_movimentacao = movimentacao.find_element(By.CLASS_NAME, 'dataMovimentacao').text
            descricao_movimentacao = movimentacao.find_element(By.CLASS_NAME, 'descricaoMovimentacao').text

            informacoes['Movimentações'].append({
                'Data de Movimentação': data_movimentacao,
                'Descrição da Movimentação': descricao_movimentacao
            })
    except:
        pass

    informacoes_processos.append(informacoes)

# Imprime as informações coletadas no formato desejado
for processo in informacoes_processos:
    print("Informações do Processo:")
    for chave, valor in processo.items():
        if chave == 'Movimentações':
            print("Movimentações:")
            for movimentacao in valor:
                print(f"Data de Movimentação: {movimentacao['Data de Movimentação']}")
                print(f"Descrição da Movimentação: {movimentacao['Descrição da Movimentação']}")
        else:
            print(f"{chave}: {valor}")
    print()

# Fecha o navegador
driver.quit()
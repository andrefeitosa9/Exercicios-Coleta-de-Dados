from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions
import pandas as pd


# Configurações iniciais do Selenium e Service para o Chrome
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Perguntar ao usuário qual produto deseja buscar
busca = input('Qual moto você deseja buscar? ').strip()

# Criar a URL
URL = 'https://www.olx.com.br/autos-e-pecas/motos/estado-ce?q=' + busca


try:
    # Acesso ao site por variável URL
    driver.get(URL)

    # Carregamento da página até encontrar o Class Name de km rodados e ano de fabricação
    WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME,"olx-ad-card__labels-item"))
    )

except selenium.common.exceptions.TimeoutException as TimeoutError:
    print ("Objeto não encontrado")

except Exception as exc:
    print (exc)

else:
    html_site_selenium = driver.page_source

# Buscar os títulos dos anúncios
dados_titulos_anuncios = driver.find_elements(By.CLASS_NAME,"olx-ad-card__title-link")

# Buscar os preços dos produtos
precos_anuncios_produtos = driver.find_elements(By.CLASS_NAME,"olx-ad-card__price")

# KM e Ano de fabricação
dados_kms_anos = driver.find_elements(By.CLASS_NAME, "olx-ad-card__labels-item")

# Buscar o link do produto e atribuir a uma variável
dados_links_produtos = driver.find_elements(By.CLASS_NAME, "olx-ad-card__link-wrapper")

# Iterações para alocar os dados encontrados em listas separadas

titulos_anuncio = []
precos_produtos = []
kms_anos = []
links_produtos = []
for dado in dados_titulos_anuncios:
    titulo_temporario = dado.text
    titulos_anuncio.append(titulo_temporario)

for preco in precos_anuncios_produtos:
    preco_temporario = preco.text
    precos_produtos.append(preco_temporario)

for link in dados_links_produtos:
    link_temporario = link.get_attribute("href")
    links_produtos.append(link_temporario)

# No caso de KMs rodados e ano de fabricação, a classe na página HTML é a mesma, por isso ficam na mesma variável, por enquanto
for dados_km_ano in dados_kms_anos:
    dado_km_ano_temporario = dados_km_ano.text
    kms_anos.append(dado_km_ano_temporario)

kms_produtos = []
anos_de_fabricacao_produtos = []

# Separação de KMs rodados e ano de fabricação em duas variáveis diferentes
for i, j in enumerate(kms_anos):
    if i%2 ==0:
        kms_produtos.append(kms_anos[i])
    else:
        anos_de_fabricacao_produtos.append(kms_anos[i])

# Alocação de dados em uma lista final no formato certo para plot em CSV usando Pandas

lista_final = []
for titulo_anuncio, preco_produto, km_produto, ano_fabricacao_produto, link_produto in zip(titulos_anuncio, precos_produtos, kms_produtos, anos_de_fabricacao_produtos, links_produtos):
    lista_final.append([titulo_anuncio, preco_produto, km_produto, ano_fabricacao_produto, link_produto])


tabela_final = pd.DataFrame(lista_final, columns = ['Nome no anúncio', 'Preço', 'Kms rodados', 'Ano de Fabricação', 'Link do produto'])
print (tabela_final)

# Envio da tabela final em CSV
tabela_final.to_csv('Tabela Produtos OLX.csv', index=False)
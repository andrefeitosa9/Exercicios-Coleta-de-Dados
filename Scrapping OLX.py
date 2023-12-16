# Programa que faz uma busca de um produto automotivo e devolve um CSV com a lista de
# Nome, preço e link para o produto

import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
import pandas as pd

# Perguntar ao usuário qual produto deseja buscar
busca = input('Qual moto você deseja buscar? ').strip()

# Criar a URL
URL = ('https://www.olx.com.br/autos-e-pecas/motos/estado-ce?q=' + busca)

# Testar se o site está funcionando, tratando erro comum HTTPError usando request. Depois disso pegar o conteúdo do site e atribuir a uma variável

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

try:
    response = requests.get(URL, headers=headers)
    response.raise_for_status()
except HTTPError as exc:
    print (exc)
else:
    # Transformar o conteúdo do site em um objeto BeautifulSoap
    html_site = BeautifulSoup(response.content, 'html.parser')

# Buscar os códigos HTML dos produtos e atribuir a uma variável
html_produtos = html_site.find_all('div', attrs={'class':'olx-ad-card__content'})
lista_final = []

for html_produto in html_produtos:
    # Buscar o nome do produto e atribuir a uma variável
    nome_produto = html_produto.find('a', attrs={'class':'olx-ad-card__title-link'}).text

    # Buscar o preço do produto e atribuir a uma variável
    preco_produto = html_produto.find('h3',attrs={'class':'olx-text'}).text

    # Buscar o link do produto e atribuir a uma variável
    link_produto = html_produto.find('a', attrs={'class':'olx-ad-card__title-link'}).get('href')
    lista_temporaria = [nome_produto, preco_produto, link_produto]
    lista_final.append(lista_temporaria)

tabela_final = pd.DataFrame(lista_final, columns = ['Nome no anúncio', 'Preço', 'Link do anúncio'])
tabela_final.to_csv('Tabela Produtos OLX.csv', index=False)

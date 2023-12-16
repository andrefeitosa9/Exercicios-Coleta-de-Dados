import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
import pandas as pd

# Exercício que pega todas as notícias no GE do Fortaleza (Título e subtítulo)

URL = 'https://ge.globo.com/ce/futebol/times/fortaleza/'

# Ver se o site está funcionando

try:
    content = requests.get(URL)
    content.raise_for_status()
except HTTPError as exc:
    print (exc)
else:
    # pegar o conteúdo da página e atribuir a uma variável
    site = content.content

# Transformar o conteúdo do site (variável site) em BeatifulSoup para poder utilizar o módulo bs4
conteudo = BeautifulSoup(site, 'html.parser')

# Pegando o HTML de todas as notícias na lista

html_noticias = conteudo.find_all('div',attrs='feed-post-body')


# pegar o conteúdo do título e atribuir a uma variável
Titulos = []
Links = []
codigos_titulo_completo = []
for noticia in html_noticias:
    codigo_titulo = noticia.find('a', attrs={'class': 'feed-post-link'})
    Titulos.append(codigo_titulo.text)


# Pegar o Link da matéria

for noticia in html_noticias:
    codigo_link = noticia.find('a', attrs={'class':'feed-post-link'})
    Links.append(codigo_link.get('href'))


# pegar o conteúdo do subtítulo (se tiver) e atribuir a uma variável. Caso não tenha, atribuir none à variável
Subtitulos = []
for noticia in html_noticias:
    codigo_subtitulo = noticia.find('div', attrs={'class':'feed-post-body-resumo'})
    if codigo_subtitulo:
        Subtitulos.append(codigo_subtitulo.text)
    else:
        Subtitulos.append(None)

print ()
# criar um dicionário com título e subtítulo
lista_noticias = []
noticias = []
noticia_temp = {}
numero_de_itens = len(Titulos)

#Fazendo como dicionário
for i, j, z in zip(Titulos, Subtitulos, Links):
    noticia_temp['Título']= i
    noticia_temp['Subtítulo'] = j
    noticia_temp['Link'] = z
    noticias.append(noticia_temp)

#Fazendo como lista
for a, b, c in zip (Titulos, Subtitulos, Links):
    lista_noticias.append([a, b, c])

print (lista_noticias)
tabela_noticias = pd.DataFrame(lista_noticias, columns=["Título", "Subtítulo", "Link da matéria"])
tabela_noticias.to_csv('tabela_noticia_ge.csv', index=False)

print ()
print (noticias)

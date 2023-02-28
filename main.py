import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import math

url = 'shttps://www.kabum.com.br/computadores/notebooks?page_number=1&page_size=20&facet_filters=eyJwcmljZSI6eyJtaW4iOjEwNjMuMTgsIm1heCI6NTc5MDB9fQ==&sort=most_searched'
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0"}

site = requests.get(url, headers=headers)
soup = BeautifulSoup(site.content, 'html.parser')
qtd_itens = soup.find('div', id='listingCount').get_text().strip()

index = qtd_itens.find(' ')
qtd = qtd_itens[:index]

ultima_pagina = math.ceil(int(qtd)/ 20)

dic_produtos = {'marca':[], 'preco':[]}

for i in range(1, ultima_pagina+1):
    url_pag = f'https://www.kabum.com.br/computadores/notebooks?page_number={i}&page_size=20&facet_filters=eyJwcmljZSI6eyJtaW4iOjEwNjMuMTgsIm1heCI6NTc5MDB9fQ==&sort=most_searched'
    site = requests.get(url_pag, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    produtos = soup.find_all('div', class_=re.compile('productCard'))

    for produto in produtos:
        marca = produto.find('span', class_=re.compile('nameCard')).get_text().strip()
        preco = produto.find('span', class_=re.compile('priceCard')).get_text().strip()

        print(marca, preco)

        dic_produtos['marca'].append(marca)
        dic_produtos['preco'].append(preco)

    print(url_pag)


df = pd.DataFrame(dic_produtos)
df.to_csv('EndereçoDeOndeDesejaColocarNoComputador/notebooks.csv', encoding='utf-8', sep=';')

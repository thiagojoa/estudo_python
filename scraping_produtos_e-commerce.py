# -*- coding: utf-8 -*-
'''
Antes gostaria de dizer que sou entusiasta python e ainda estou aprendendo a utiliza-lo,
em resumo quero dizer que todas as sugestões, correções etc, serão bem vindas

Código desenvolvido para mostrar exemplo de um crawler que obtem dados
de produtos de um E-commerce

Eu particularmente divido o processo de scraping nas seguintes etapas:
1 - Compreensão do alvo, isto é, quais dados queremos obter
2 - Localização do alvo, isto é, onde estão os dados dentro do html
3 - Identificação do método de estração, por exemplo, o alvo esta dentro de tags htmls?
ou esta dentro de um script javascript? Como o alvo esta no codigo?
4- Obtenção dos dados com a ferramenta escolhida.

Neste exemplo usaremos a página de uma churrasqueira de um e-commerce para obter os seguintes dados

Titulo da Pagina do produto:
Descrição do produto:
Preço:
Marca:
Categoria:
SKU:

O HTML desta pagina, esta disponivel na raiz do github para análise com o Nome
pagina_churraqueira_nautika.html ou no link https://www.lojasestrela.com.br/churrasqueira-nautika-colorado

Neste caso fica claro que o alvo, isto é, os dados que queremos obter,
estão dentro de uma tag <script> dentro do <head> do HTML

Como dentro da TAG <Script> existe um conjunto de dados do tipo JSON,
a biblioteca BeautifulSoup tem uma limitação conseguindo capturar apenas o conteudo de tags html
isto é, não será possível tratar o conteudo de dentro da tag <script> com a BeautifulSoup,
para isso, usarei no exemplo, tratamentos de string com Regex. Expressões Regulares


Então mostrarei como capturar estes dados

---

Autor: Thiago M. S. Bueno
thiago.msbueno@gmail.com

'''

#Primeiramente vamos importar o requests, que é a lib que vai pegar o HTML para nós
import requests

#Depois importaremos a lib BeautifulSoup, que irá capturar dados dentro do html
#Vou apelidar a lib BeautifulSoup como bs para ficar mais facil as chamadas futuras
from bs4 import BeautifulSoup as bs

#Agora importaremos a biblioteca Regex, para capturarmos os dados de acordo com nosso alvo
import re

'''
#O site que iremos capturar as informações será o E-commerce das Loajs Estrela http://www.lojasestrela.com.br
#O produto será a churrasqueira nautika, https://www.lojasestrela.com.br/churrasqueira-nautika-colorado
'''

#html é a variavel que vai armazenar o conteúdo html da pagina
html = requests.get('https://www.lojasestrela.com.br/churrasqueira-nautika-colorado')

#Gerando o objeto BeautifulSoup com o conteudo da variavel html
soup = bs(html.content, "lxml")

#agora, convertemos o o objeto retornado em string para utilizarmos com o regex
string_html = str(soup.html.head)

#print(soup.html.head) #teremos a saida do head do html

#Agora faremos a busca via regex dos dados alvo
#Foi verificado que o alvo esta dentro do trecho de Codigo
#'<script>dataLayer=......' sendo assim o codigo regex que da
#match no preço por exemplo é ""priceSell":"(.\w.\w*[.]\w*)/"
#voce pode checar essa regex no site https://www.regexpal.com/

#Capturando o preço do produto com regex

#capturando o titulo da pagina, sabendo que ja temos ele no objeto
#Soup, podendo então capturalo através do HTML -> HEAD - > TITLE
#porem vamos utilizar o find para ser mais um exemplo
titulo_pagina = soup.find('title')

#Agora transformar a var em string para remover tags html e utilização posterior
titulo_pagina = str(titulo_pagina)

#Cria varial com codigo regex que remove tags html de strings
TAG_RE = re.compile(r'<[^>]+>')

#cria-se função que remove tags html de strings
def remove_tags(text):
    return TAG_RE.sub('', text)

#remove as tags html chamando a funcao que remove tags e pronto
#nossa variavel titulo_pagina agora é uma string sem tags htmls
titulo_pagina = remove_tags(titulo_pagina)

#capturando a descricao do produtos com find regex
descricao = re.findall(r'(?:"nameProduct":")(.*?)(?:")', string_html)
#Agora transformar a var em string para utilização posterior
descricao = str(descricao)

#capturando preço do produto com find regex
preco = re.findall(r'"priceSell":"(.\w*[.]\w*)', string_html)
#Agora transformar a var em string para utilização posterior
preco = str(preco)

#capturando a marca do produto com find regex
marca = re.findall(r'(?:"brand":")(.*?)(?:")', string_html)
#Agora transformar a var em string para utilização posterior
marca = str(marca)

#capturando a categoria do produto com find regex
categoria = re.findall(r'(?:"brand":")(.*?)(?:")', string_html)
#Agora transformar a var em string para utilização posterior
categoria = str(categoria)

#capturando o SKU do produto com find regex
sku= re.findall(r'(?:"idProduct":")(.*?)(?:")', string_html)
#Agora transformar a var em string para utilização posterior
sku = str(sku)

print('Título da Página: '+ titulo_pagina)
print('Descrição do Produto: '+ descricao)
print('Preço: '+ preco)
print('Marca: '+ marca)
print('Sku: '+sku)

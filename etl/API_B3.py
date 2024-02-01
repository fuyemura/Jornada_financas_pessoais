from chave_api import *
import pprint
import requests
import pandas as pd
from io import StringIO

# Conectando com URL site: "Alpha Vantage"
chave = chave_api('7J5LMKLOTVO7A7Z6')
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={cotacao_empresa}&apikey={chave}&datatype=csv'
r = requests.get(url)
dados = r.text
print(dados)
tabela = pd.read_csv(StringIO(r.text))
print(tabela)

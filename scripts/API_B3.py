from chave_api import *
import pprint
import requests
import pandas as pd
from io import StringIO

# Conectando com URL site: "Alpha Vantage"
chave = chave_api('ZAS64M81QA0U6TMD')
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={cotacao_empresa}&apikey={chave}&datatype=csv'
r = requests.get(url)
dados = r.text
# Transformando retorno API em arquivo e lendo em csv
tabela = pd.read_csv(StringIO(dados))
df = pd.DataFrame(tabela, index=None)
print(df)


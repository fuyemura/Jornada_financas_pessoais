import pandas as pd
from conexao_banco_de_dados import conexao_mysql
# cotahist SQL:
cotahist = pd.read_sql_query('SELECT*FROM bronze.cotahist', con=conexao_mysql('bronze'))
cotahist['data_pregao'] = pd.to_datetime(cotahist['data_pregao'], format='%Y%m%d')
cotahist['preco_abertura_papel'] = cotahist['preco_abertura_papel']/100
cotahist['preco_maximo_papel'] = cotahist['preco_maximo_papel']/100
cotahist['preco_minimo_papel'] = cotahist['preco_minimo_papel']/100
cotahist['preco_medio_papel'] = cotahist['preco_medio_papel']/100
cotahist['preco_ultimo_negocio'] = cotahist['preco_ultimo_negocio']/100
cotahist['preco_melhor_oferta_compra'] = cotahist['preco_melhor_oferta_compra']/100
cotahist['preco_melhor_oferta_venda'] = cotahist['preco_melhor_oferta_venda']/100

# Conexão com o banco de dados na camada "silver":
engine = conexao_mysql('silver')
data_frame = cotahist.to_sql(name='cotahist', con=engine, if_exists='replace', index=False)
if (data_frame):
    print('\033[1;32mDados gravados com sucesso!\033[m')
else:
    print('\033[1;31mHouve algum problema!\033[m')

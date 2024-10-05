import pandas as pd
from pipeline.conexao_bancodedados import conexao_mysql
posicaocolumn = [(1, 2), (2, 10), (10, 12), (12, 18), (25, 27), (27, 39), (47, 49), (50, 52), (53, 56), (57, 69), (70, 82), (83, 95), (96, 108), (109, 121), (122, 134), (135, 147), (148, 152), (153, 170), (171, 188), (189, 201), (202, 202), (203, 210), (211, 217), (218, 230), (231, 242), (243, 245)]
namescolumn = ['tipo_registro',
               'data_pregao',
               'codigo_bdi',
               'codigo_negociacao',
               'tipo_mercado',
               'nome_resumido_empresa',
               'especificacao_papel',
               'prazo_dias_mercado',
               'moeda_referencia',
               'preco_abertura_papel',
               'preco_maximo_papel',
               'preco_minimo_papel',
               'preco_medio_papel',
               'preco_ultimo_negocio',
               'preco_melhor_oferta_compra',
               'preco_melhor_oferta_venda',
               'numero_negocios_efetuados',
               'quantidade_total_titulos',
               'volume_total_titulos',
               'preco_exercicio_opcoes',
               'indicador_correcao_precos',
               'data_vencimento_opcoes',
               'fator_cotacao_papel',
               'preco_exercicio_pontos',
               'codigo_papel_sistema',
               'numero_distribuicao_papel']
df = pd.read_fwf('../data/COTAHIST_A2023.txt', index_col=None, colspecs=posicaocolumn, names=namescolumn, skiprows=1, skipfooter=1)
pd.DataFrame(df)

# Conexão com o banco de dados na camada "bronze":
engine = conexao_mysql('bronze')
df.to_sql(name='cotahist', con=engine, if_exists='replace', index=False)













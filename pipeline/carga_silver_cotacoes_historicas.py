import pandas as pd
from conexao_banco_de_dados import conexao_mysql

# Consulta SQL:
consulta = pd.read_sql_table('cotahist', con=conexao_mysql('bronze'))

# Conexão com o banco de dados na camada "silver":
engine = conexao_mysql('silver')
data_frame = consulta.to_sql(name='cotahist', con=engine, if_exists='replace', index=False)
if (data_frame):
    print('\033[1;32mDados gravados com sucesso!\033[m')
else:
    print('\033[1;31mHouve algum problema!\033[m')

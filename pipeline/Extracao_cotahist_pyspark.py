
from pyspark.sql import SparkSession
from pyspark.sql.functions import substring
from datetime import date
from conexao import *

ano = date.today().year
# Inicializa uma SparkSession
spark = SparkSession.builder \
    .appName("Leitura de Arquivo de Formato Fixo") \
    .getOrCreate()

# Define as posições iniciais e finais de cada campo
positions = {"tipo_registro": (1, 2),
               "data_pregao": (3, 10),
               "codigo_bdi": (11, 12),
               "codigo_negociacao": (13, 24),
               "tipo_mercado": (25, 27),
               "nome_resumido_empresa": (28, 39),
               "especificacao_papel": (40, 49),
               "prazo_dias_mercado": (50, 52),
               "moeda_referencia": (53, 56),
               "preco_abertura_papel": (57, 69),
               "preco_maximo_papel": (70, 82),
               "preco_minimo_papel": (83, 95),
               "preco_medio_papel": (96, 108),
               "preco_ultimo_negocio": (109, 121),
               "preco_melhor_oferta_compra": (122, 134),
               "preco_melhor_oferta_venda": (135, 147),
               "numero_negocios_efetuados": (148, 152),
               "quantidade_total_titulos": (153, 170),
               "volume_total_titulos": (171, 188),
               "preco_exercicio_opcoes": (189, 201),
               "indicador_correcao_precos": (202, 202),
               "data_vencimento_opcoes": (203, 210),
               "fator_cotacao_papel": (211, 217),
               "preco_exercicio_pontos": (218, 230),
               "codigo_papel_sistema": (231, 242),
               "numero_distribuicao_papel": (243, 245)
			   }

# Caminho do arquivo de entrada
file_path = r'C:\Users\Lucas\OneDrive\Documentos\projetos_python\Jornada_financas_pessoais\data\COTAHIST_A2024.TXT'

# Lê o arquivo de formato fixo
df = spark.read.text(file_path)

# Extrai os campos em formato fixo usando a função substring
for field, (start, end) in positions.items():
    df = df.withColumn(field, substring("value", start, end - start + 1))

# Filtrar os registros com tipo do registro igual a 1
df = df.filter(df["tipo_registro"] == "01")    

# Remove a coluna "value" original
df = df.drop("value")

# Configurações para conexão com o banco de dados MySQL
jdbc_url = connection(database="silver")
jdbc_mode = "overwrite"  # Sobrescreve a tabela se ela já existir
jdbc_properties = properties()
table = 'cotacoes_historicas'

# Escreve o DataFrame no banco de dados MySQL
df.write.jdbc(url=jdbc_url, table=table, mode=jdbc_mode, properties=jdbc_properties)

# Mostra o DataFrame resultante
#df.show()

# Ler tabela do MySQL Workbeench em um DataFrame
df_sql = spark.read\
.format("jdbc")\
.option("driver", "com.mysql.cj.jdbc.Driver")\
.option("url", jdbc_url)\
.option("query", "SELECT * FROM bronze.cotahist")\
.option("user", "financasp")\
.option("password", "Financasp#321")\
.load()

df_sql.show()



# Encerra a SparkSession
spark.stop()


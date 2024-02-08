from pyspark.sql import SparkSession
from pyspark.sql.functions import substring
from datetime import date

ano = date.today().year

# Inicializa uma SparkSession
spark = SparkSession.builder \
    .appName("Leitura de Arquivo de Formato Fixo") \
    .getOrCreate()

# Define as posições iniciais e finais de cada campo
positions = {"tipo_registro": (1, 2),
               "data_pregao": (2, 10),
               "codigo_bdi": (10, 12),
               "codigo_negociacao": (12, 18),
               "tipo_mercado": (25, 27),
               "nome_resumido_empresa": (27, 37),
               "especificacao_papel": (38, 49),
               "prazo_dias_mercado": (50, 51),
               "moeda_referencia": (52, 56),
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
               "indicador_correcao_precos": (200, 202),
               "data_vencimento_opcoes": (203, 210),
               "fator_cotacao_papel": (211, 217),
               "preco_exercicio_pontos": (218, 229),
               "codigo_papel_sistema": (230, 240),
               "numero_distribuicao_papel": (242, 245)
			   }

# Caminho do arquivo de entrada
file_path = f'data/COTAHIST_A{ano}.TXT'

# Lê o arquivo de formato fixo
df = spark.read.text(file_path)

# Extrai os campos em formato fixo usando a função substring
for field, (start, end) in positions.items():
    df = df.withColumn(field, substring("value", start, end - start + 1))

# Remove a coluna "value" original
df = df.drop("value")


# Configurações para conexão com o banco de dados MySQL
jdbc_url = "jdbc:mysql://localhost:3306/bronze"
mode = "overwrite"  # Sobrescreve a tabela se ela já existir
properties = {
    "user": "financasp",
    "password": "Financasp#321",
    "driver": "com.mysql.cj.jdbc.Driver"
}

# Escreve o DataFrame no banco de dados MySQL
df.write.jdbc(url=jdbc_url, table="cotahist", mode=mode, properties=properties)

# Mostra o DataFrame resultante
#df.show()

# Encerra a SparkSession
spark.stop()

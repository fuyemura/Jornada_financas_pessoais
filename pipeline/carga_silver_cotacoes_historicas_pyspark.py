from pyspark.sql import SparkSession
from pyspark.sql.functions import to_date, col
from pyspark.sql.types import DecimalType
from conexao_bancodedados import *

# Criação da SparkSession
spark = SparkSession.builder \
    .appName("Leitura e Transformação MySQL") \
    .config("spark.executor.memory", "4g") \
    .config("spark.driver.memory", "2g") \
    .getOrCreate()

# Configurações para conexão com o banco de dados MySQL
jdbc_url = connection("bronze")
jdbc_properties = properties()

# Lendo a tabela MySQL no DataFrame do PySpark
df = spark.read.jdbc(url=jdbc_url, table='cotahist', properties=jdbc_properties)

# Transformação dos dados
df_transformado = df.withColumn("data_pregao", to_date(col("data_pregao"), "yyyyMMdd")) \
                    .withColumn("preco_abertura_papel", col("preco_abertura_papel").cast("float") / 100) \
                    .withColumn("preco_maximo_papel", col("preco_maximo_papel").cast("float") / 100) \
                    .withColumn("preco_minimo_papel", col("preco_minimo_papel").cast("float") / 100) \
                    .withColumn("preco_medio_papel", col("preco_medio_papel").cast("float") / 100) \
                    .withColumn("preco_ultimo_negocio", col("preco_ultimo_negocio").cast("float") / 100) \
                    .withColumn("preco_melhor_oferta_compra", col("preco_melhor_oferta_compra").cast("float") / 100) \
                    .withColumn("preco_melhor_oferta_venda", col("preco_melhor_oferta_venda").cast("float") / 100) \
                    .withColumn("volume_total_titulos", col("volume_total_titulos").cast("float") / 100) \
                    .withColumn("preco_exercicio_opcoes", col("preco_exercicio_opcoes").cast("float") / 100) \
                    .withColumn("preco_exercicio_pontos", col("preco_exercicio_pontos").cast(DecimalType(7, 6)) / 1000000)

# Truncar os dados da tabela antes de carregar
truncate_table('silver','cotacoes_historicas')

# Escrever os dados transformados de volta para outra tabela no MySQL
jdbc_url = connection("silver")
jdbc_mode = "append"  # Insere os dados na tabela
jdbc_properties = properties()

# Escreve o DataFrame no banco de dados MySQL
df_transformado.write.jdbc(url=jdbc_url, table='cotacoes_historicas', mode=jdbc_mode, properties=jdbc_properties)

# Encerra a SparkSession
spark.stop()
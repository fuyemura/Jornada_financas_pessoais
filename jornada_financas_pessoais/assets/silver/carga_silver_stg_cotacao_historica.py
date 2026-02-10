from dagster import asset, AssetKey, MaterializeResult, MetadataValue
from pyspark.sql import functions as F
from pyspark.sql.types import DecimalType, IntegerType

from jornada_financas_pessoais.config.partitions import ANO_PARTITIONS
from jornada_financas_pessoais.config.paths import BRONZE_PATHS, SILVER_PATHS

BRONZE_PATH = BRONZE_PATHS["raw_cotahist"]
SILVER_PATH = SILVER_PATHS["stg_cotacao_historica"]


@asset(
    name="stg_cotacao_historica",
    key_prefix=["silver"],
    compute_kind="spark",
    description="Transforma a cotação histórica da Bronze para Silver",
    required_resource_keys={"spark"},
    partitions_def=ANO_PARTITIONS,
    deps=[AssetKey(["bronze", "raw_cotahist"])]
)
def stg_cotacao_historica(context):
    spark = context.resources.spark
    ano = context.partition_key

    # Leitura do Bronze por partição do ano
    TABLE_BRONZE_PATH_ANO = f"{BRONZE_PATH}/ano={ano}"
    
    context.log.info(f"Lendo Bronze {TABLE_BRONZE_PATH_ANO}")

    try:
        df_bronze = spark.read.format("delta").load(TABLE_BRONZE_PATH_ANO)
    except Exception as e:
        context.log.warning(f"Nenhum dado encontrado para o ano {ano}: {e}")
        return MaterializeResult(
            metadata={
                "processamento": MetadataValue.json({
                    "ano": ano,
                    "registros": 0,
                    "status": "sem dados"
                })
            }
        )

    total_registros = df_bronze.count()
    context.log.info(f"{total_registros} registros encontrados na Bronze para {ano}")

    # Transformações para Silver
    df_silver = df_bronze.select(
        F.col("tipo_registro").cast("string").alias("tp_registro"),
        F.to_date(F.col("data_pregao"), "yyyyMMdd").alias("dt_pregao"),
        F.col("codigo_bdi").cast("string").alias("cd_bdi"),
        F.trim(F.col("codigo_negociacao")).alias("cd_negociacao"),
        F.col("tipo_mercado").cast("string").alias("tp_mercado"),
        F.trim(F.col("nome_resumido_empresa")).alias("nm_empresa"),
        F.trim(F.col("especificacao_papel")).alias("ds_especificacao_papel"),
        F.col("prazo_dias_mercado").cast("string").alias("nr_prazo_dias_mercado"),
        F.col("moeda_referencia").cast("string").alias("cd_moeda_referencia"),
        (F.col("preco_abertura_papel") / 100).cast(DecimalType(11,2)).alias("vl_abertura"),
        (F.col("preco_maximo_papel") / 100).cast(DecimalType(11,2)).alias("vl_maximo"),
        (F.col("preco_minimo_papel") / 100).cast(DecimalType(11,2)).alias("vl_minimo"),
        (F.col("preco_medio_papel") / 100).cast(DecimalType(11,2)).alias("vl_medio"),
        (F.col("preco_ultimo_negocio") / 100).cast(DecimalType(11,2)).alias("vl_ultimo_negocio"),
        (F.col("preco_melhor_oferta_compra") / 100).cast(DecimalType(11,2)).alias("vl_melhor_oferta_compra"),
        (F.col("preco_melhor_oferta_venda") / 100).cast(DecimalType(11,2)).alias("vl_melhor_oferta_venda"),
        F.col("numero_negocios_efetuados").cast(IntegerType()).alias("qt_negocios_efetuados"),
        F.col("quantidade_total_titulos").cast(IntegerType()).alias("qt_total_titulos"),
        (F.col("volume_total_titulos") / 100).cast(DecimalType(16,2)).alias("vl_total_titulos"),
        (F.col("preco_exercicio_opcoes") / 100).cast(DecimalType(11,2)).alias("vl_exercicio_opcoes"),
        F.col("indicador_correcao_precos").cast("string").alias("cd_indicador_correcao"),
        F.to_date(F.col("data_vencimento_opcoes"), "yyyyMMdd").alias("dt_vencimento_opcoes"),
        F.col("fator_cotacao_papel").cast("string").alias("cd_fator_cotacao"),
        (F.col("preco_exercicio_pontos") / 1000000).cast(DecimalType(7,6)).alias("vl_exercicio_pontos"),
        F.col("codigo_papel_sistema").cast("string").alias("cd_papel_sistema"),
        F.col("numero_distribuicao_papel").cast("string").alias("nr_distribuicao_papel"),
        F.col("nome_arquivo").cast("string").alias("nm_arquivo_origem"),
        F.lit(ano).alias("ds_ano"),  # coluna de partição
        F.current_timestamp().alias("ts_insercao")
    )

    # Gravação na Silver, garantindo partição por ano
    (
    df_silver.write.format("delta")
        .mode("overwrite")
        .partitionBy("ds_ano")
        .option("overwriteSchema", "false")
        .save(SILVER_PATH)
    )    

    context.log.info(f"Silver gravada em: {SILVER_PATH} para o ano {ano}")

    return MaterializeResult(
        metadata={
            "processamento": MetadataValue.json({
                "ano": ano,
                "registros": total_registros,
                "destino": SILVER_PATH
            })
        }
    )

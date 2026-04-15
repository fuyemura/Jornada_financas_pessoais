from dagster import asset, AssetKey, MaterializeResult, MetadataValue
from pyspark.sql import functions as F

from jornada_financas_pessoais.config.partitions import ANO_PARTITIONS
from jornada_financas_pessoais.config.paths import SILVER_PATHS, GOLD_PATHS

SILVER_PATH = SILVER_PATHS["stg_cotacao_historica"]
DIM_PATH = GOLD_PATHS["dim_ativo_financeiro"]
FATO_PATH = GOLD_PATHS["fato_cotacao"]


@asset(
    name="fato_cotacao",
    key_prefix=["gold"],
    compute_kind="spark",
    description="Fato de cotações de ativos (Star Schema)",
    required_resource_keys={"spark"},
    partitions_def=ANO_PARTITIONS,
    deps=[AssetKey(["silver", "stg_cotacao_historica"]), AssetKey(["gold", "dim_ativo_financeiro"])],
    op_tags={"dagster/max_retries": 2},
)
def fato_cotacao(context):
    spark = context.resources.spark

    # Ano da partição Dagster
    ano = context.partition_key

    context.log.info(f"Lendo Silver {SILVER_PATH} para o ano {ano}")

    # Leitura Silver (somente partição necessária)
    df_stg = (
        spark.read.format("delta")
        .load(SILVER_PATH)
        .filter(F.col("ano_particao") == ano)
    )

    context.log.info(f"Lendo Dimensão {DIM_PATH}")

    df_dim = spark.read.format("delta").load(DIM_PATH)

    context.log.info(f"{df_stg.count()} registros encontrados na Silver para o ano {ano}")
    context.log.info(f"{df_dim.count()} registros encontrados na Dimensão")

    # --- Transformação ---
    df_stg = df_stg.filter(F.col("tipo_mercado") == "010")
    
    df_fato = (
        df_stg.alias("stg")
        .join(
            df_dim.alias("dim"),
            F.col("stg.codigo_negociacao") == F.col("dim.codigo_ativo"),
            "left"
        )
        .select(
            F.col("stg.data_pregao"),
            F.coalesce(F.col("id_ativo_financeiro"), F.lit(-1)).alias("id_ativo_financeiro"),
            F.col("preco_abertura_papel").alias("preco_abertura"),
            F.col("preco_minimo_papel").alias("preco_minimo"),
            F.col("preco_maximo_papel").alias("preco_maximo"),
            F.col("preco_medio_papel").alias("preco_medio"),
            F.col("preco_ultimo_negocio").alias("preco_ultimo_negocio"),
            F.col("numero_negocios_efetuados").alias("quantidade_negocio"),
            F.col("quantidade_total_titulos").alias("quantidade_titulo"),
            F.col("volume_total_titulos").alias("volume_financeiro"),
            F.lit(ano).alias("ano_particao"),  # partição física
            F.current_timestamp().alias("criado_em"),
        )
    )

    total_registros = df_fato.count()

    if total_registros == 0:
        raise Exception(f"Nenhum registro processado para o ano {ano}")

    # Gravação idempotente por partição do ano, garantindo que reprocessamentos não causem duplicidade
    (
        df_fato.write.format("delta")
        .mode("overwrite")
        .option("replaceWhere", f"ano_particao = {ano}")
        .partitionBy("ano_particao")
        .save(FATO_PATH)
    )

    context.log.info(f"Gold gravada em {FATO_PATH} para o ano {ano}")

    return MaterializeResult(
        metadata={
            "processamento": MetadataValue.json({
                "ano": ano,
                "registros": total_registros,
                "destino": FATO_PATH
            })
        }
    )
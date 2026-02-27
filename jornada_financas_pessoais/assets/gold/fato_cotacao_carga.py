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
    op_tags={"dagster/max_retries": "2"},
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
        .filter(F.col("ds_ano") == ano)
    )

    context.log.info(f"Lendo Dimensão {DIM_PATH}")

    df_dim = spark.read.format("delta").load(DIM_PATH)

    context.log.info(f"{df_stg.count()} registros encontrados na Silver para o ano {ano}")
    context.log.info(f"{df_dim.count()} registros encontrados na Dimensão")

    # --- Transformação ---
    df_stg = df_stg.filter(F.col("tp_mercado") == "010")
    
    df_fato = (
        df_stg.alias("stg")
        .join(
            df_dim.alias("dim"),
            F.col("stg.cd_negociacao") == F.col("dim.cd_ativo"),
            "left"
        )
        .select(
            F.col("stg.dt_pregao"),
            F.coalesce(F.col("sk_ativo"), F.lit(-1)).alias("sk_ativo"),
            F.col("vl_abertura"),
            F.col("vl_minimo"),
            F.col("vl_maximo"),
            F.col("vl_medio"),
            F.col("vl_ultimo_negocio"),
            F.col("qt_negocios_efetuados").alias("qt_negocio"),
            F.col("qt_total_titulos").alias("qt_titulo"),
            F.col("vl_total_titulos").alias("vl_volume"),
            F.lit(ano).alias("ds_ano"),  # partição física
            F.current_timestamp().alias("ts_insercao"),
        )
    )

    total_registros = df_fato.count()

    if total_registros == 0:
        raise Exception(f"Nenhum registro processado para o ano {ano}")

    # Gravação idempotente por partição do ano, garantindo que reprocessamentos não causem duplicidade
    (
        df_fato.write.format("delta")
        .mode("overwrite")
        .option("replaceWhere", f"ds_ano = {ano}")
        .partitionBy("ds_ano")
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
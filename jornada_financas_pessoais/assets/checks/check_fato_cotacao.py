from dagster import asset_check, AssetCheckResult
from pyspark.sql import functions as F

from jornada_financas_pessoais.config.partitions import ANO_PARTITIONS
from jornada_financas_pessoais.config.paths import GOLD_PATHS

FATO_PATH = GOLD_PATHS["fato_cotacao"]


@asset_check(
    asset="gold/fato_cotacao",
    partitions_def=ANO_PARTITIONS,
)
def check_sk_ativo_valida(context):
    spark = context.resources.spark
    ano = context.partition_key

    df = (
        spark.read.format("delta")
        .load(FATO_PATH)
        .filter(F.col("ds_ano") == ano)
    )

    invalid = df.filter(F.col("sk_ativo") == -1).count()

    return AssetCheckResult(
        passed=invalid == 0,
        metadata={"registros_invalidos": invalid}
    )

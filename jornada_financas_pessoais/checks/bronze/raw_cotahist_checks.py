from dagster import asset_check, AssetCheckResult
from pyspark.sql import functions as F

from jornada_financas_pessoais.config.paths import BRONZE_PATHS

BRONZE_PATH = BRONZE_PATHS["raw_cotahist"]

def carregar_raw_cotahist(context):
    ano = context.partition_key  # pega o ano da partição atual, ex: "2017"
    return (
        context.resources.spark.read
        .format("delta")
        .load(BRONZE_PATH)
        .filter(F.col("ano") == ano)  # ajuste o nome da coluna de partição
    )


@asset_check(
    asset=["bronze", "raw_cotahist"],
    blocking=True,
    description="Bronze não pode estar vazia",
    required_resource_keys={"spark"}
)
def raw_cotahist_nao_vazio(context):
    df = carregar_raw_cotahist(context)
    row_count = df.count()

    return AssetCheckResult(
        passed=row_count > 0,
        metadata={"row_count": row_count}
    )


@asset_check(
    asset=["bronze", "raw_cotahist"],
    blocking=True,
    description="Data de pregão não pode ser nula",
    required_resource_keys={"spark"}
)
def raw_cotahist_sem_datas_nulas(context):
    df = carregar_raw_cotahist(context)
    null_count = df.filter(
        F.col("data_pregao").isNull()
    ).count()

    return AssetCheckResult(
        passed=null_count == 0,
        metadata={"datas_nulas": null_count}
    )
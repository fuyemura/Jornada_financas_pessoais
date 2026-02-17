from dagster import asset_check, AssetCheckResult
from pyspark.sql import functions as F

from jornada_financas_pessoais.config.paths import SILVER_PATHS

SILVER_PATH = SILVER_PATHS["stg_cotacao_historica"]

def carregar_stg_cotacao_historica(context):
    ano = context.partition_key  # pega o ano da partição atual, ex: "2017"
    return (
        context.resources.spark.read
        .format("delta")
        .load(SILVER_PATH)
        .filter(F.col("ds_ano") == ano)  # ajuste o nome da coluna de partição
    )


@asset_check(
    asset=["silver", "stg_cotacao_historica"],
    blocking=True,
    description="Silver não pode estar vazia",
    required_resource_keys={"spark"}
)
def stg_cotacao_historica_nao_vazio(context):
    df = carregar_stg_cotacao_historica(context)
    count = df.count()

    return AssetCheckResult(
        passed=count > 0,
        metadata={"row_count": count}
    )


@asset_check(
    asset=["silver", "stg_cotacao_historica"],
    blocking=True,
    description="Não pode haver dt_pregao nula",
    required_resource_keys={"spark"}
)
def stg_cotacao_historica_sem_data_nula(context):
    df = carregar_stg_cotacao_historica(context)

    nulls = df.filter(
        F.col("dt_pregao").isNull()
    ).count()

    return AssetCheckResult(
        passed=nulls == 0,
        metadata={"datas_nulas": nulls}
    )

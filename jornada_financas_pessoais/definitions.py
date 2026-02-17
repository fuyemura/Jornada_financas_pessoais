from dagster import Definitions

# Import dos assets
from jornada_financas_pessoais.assets.bronze.ingestao_bronze_raw_cotahist import raw_cotahist
from jornada_financas_pessoais.assets.silver.carga_silver_stg_cotacao_historica import stg_cotacao_historica
from jornada_financas_pessoais.assets.gold.carga_gold_dim_ativo_financeiro import dim_ativo_financeiro
from jornada_financas_pessoais.assets.gold.carga_gold_fato_cotacao import fato_cotacao
from jornada_financas_pessoais.checks.gold.fato_cotacao_checks import check_sk_ativo_valida
from jornada_financas_pessoais.jobs.financas_pessoais import financas_pessoais_job

# Import do Spark resource
from jornada_financas_pessoais.resources.spark_resource import resource_spark

# Definição do pipeline (Definitions)
defs = Definitions(
    assets=[
        raw_cotahist,
        stg_cotacao_historica,
        dim_ativo_financeiro,
        fato_cotacao,
        ],
    asset_checks=[
        check_sk_ativo_valida,
        ],
    jobs=[financas_pessoais_job],
    resources={
        "spark": resource_spark
    }
)
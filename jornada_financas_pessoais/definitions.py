from dagster import Definitions

# Import dos assets
from jornada_financas_pessoais.assets.bronze.ingestao_bronze_raw_cotahist import raw_cotahist
from jornada_financas_pessoais.assets.silver.carga_silver_stg_cotacao_historica import stg_cotacao_historica
from jornada_financas_pessoais.assets.gold.carga_gold_dim_ativo_financeiro import dim_ativo_financeiro


# Import do Spark resource
from jornada_financas_pessoais.resources.spark_resource import resource_spark

# Definição do pipeline (Definitions)
defs = Definitions(
    assets=[
        raw_cotahist,
        stg_cotacao_historica,
        dim_ativo_financeiro
        ],
    resources={
        "spark": resource_spark
    }
)
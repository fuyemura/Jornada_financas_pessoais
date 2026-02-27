from dagster import Definitions

# Import dos assets
from jornada_financas_pessoais.assets.bronze.raw_cotahist_ingestao import raw_cotahist
from jornada_financas_pessoais.sensors.raw_cotahist_sensor import raw_cotahist_file_sensor
from jornada_financas_pessoais.checks.bronze.raw_cotahist_checks import (
    check_raw_cotahist_arquivo_fonte_existe,
    check_raw_cotahist_schema_contrato,
    check_raw_cotahist_sanidade_arquivo,
)
from jornada_financas_pessoais.assets.silver.stg_cotacao_historica_carga import stg_cotacao_historica
from jornada_financas_pessoais.checks.silver.stg_cotacao_historica_checks import (
    stg_cotacao_historica_nao_vazio,
    stg_cotacao_historica_sem_data_nula,
)
from jornada_financas_pessoais.assets.gold.dim_ativo_financeiro_carga import dim_ativo_financeiro
from jornada_financas_pessoais.assets.gold.fato_cotacao_carga import fato_cotacao
from jornada_financas_pessoais.checks.gold.fato_cotacao_checks import fato_cotacao_sk_ativo_valida
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
        check_raw_cotahist_arquivo_fonte_existe,
        check_raw_cotahist_schema_contrato,
        check_raw_cotahist_sanidade_arquivo,
        stg_cotacao_historica_nao_vazio,
        stg_cotacao_historica_sem_data_nula,
        fato_cotacao_sk_ativo_valida,
        ],
    sensors=[raw_cotahist_file_sensor],
    jobs=[financas_pessoais_job],
    resources={
        "spark": resource_spark
    }
)
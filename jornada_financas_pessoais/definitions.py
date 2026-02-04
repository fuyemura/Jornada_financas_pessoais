from dagster import Definitions

from jornada_financas_pessoais.assets.bronze.ingestao_bronze_raw_cotahist import raw_cotahist
from jornada_financas_pessoais.resources.spark_resource import resource_spark

defs = Definitions(
    assets=[raw_cotahist],
    resources={
        "spark": resource_spark
    }
)

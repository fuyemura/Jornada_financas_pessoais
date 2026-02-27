from dagster import resource
from jornada_financas_pessoais.utils.spark_config import init_spark

@resource
def resource_spark(_):
    spark = init_spark("Dagster-Financas-Pessoais")
    try:
        yield spark
    finally:
        spark.stop()
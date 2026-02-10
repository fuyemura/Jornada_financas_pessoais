import glob
import os

from dagster import asset, MaterializeResult, MetadataValue
from pyspark.sql import functions as F

from jornada_financas_pessoais.config.partitions import ANO_PARTITIONS
from jornada_financas_pessoais.config.paths import SOURCE_PATHS, BRONZE_PATHS
from jornada_financas_pessoais.utils.cotahist_parser import parse_cotahist

SOURCE_PATH = SOURCE_PATHS["cotahist"]
BRONZE_PATH = BRONZE_PATHS["raw_cotahist"]


@asset(
    name="raw_cotahist",
    key_prefix=["bronze"],
    compute_kind="spark",
    description="Ingestão Bronze da cotação histórica da B3 (COTAHIST)",
    required_resource_keys={"spark"},
    partitions_def=ANO_PARTITIONS,
)
def raw_cotahist(context):
    spark = context.resources.spark
    ano = context.partition_key  # chave da partição

    # Busca apenas arquivos do ano da partição
    files = glob.glob(f"{SOURCE_PATH}/COTAHIST_A{ano}.TXT")

    if not files:
        context.log.warning(f"Nenhum arquivo encontrado para o ano {ano}")
        return MaterializeResult(
            metadata={
                "info": MetadataValue.json({
                    "ano": ano,
                    "registros": 0,
                    "status": "sem_dados"
                })
            }
        )

    context.log.info(f"{len(files)} arquivo(s) encontrados para {ano}")
    context.log.info(f"Leitura do(s) arquivo(s) {files}")

    # Transforma os arquivos de texto em DataFrame, aplicando a partição do ano
    df_raw = (
        spark.read.text(files)
        .withColumn(
            "nome_arquivo",
            F.regexp_extract(F.input_file_name(), r"[^/\\\\]+$", 0)
        )
        .withColumn("ano", F.lit(ano))  # coluna de partição
    )

    df = parse_cotahist(df_raw)

    total = df.count()
    context.log.info(f"{total} registros válidos para {ano}")

    # Gravar no Bronze, garantindo partição por ano
    (
        df.write
        .format("delta")
        .mode("overwrite")               # idempotência
        .partitionBy("ano")              # partição física
        .option("overwriteSchema", "false")
        .save(BRONZE_PATH)
    )

    return MaterializeResult(
        metadata={
            "processamento": MetadataValue.json({
                "ano": ano,
                "arquivos": [os.path.basename(f) for f in files],
                "registros": total,
                "destino": BRONZE_PATH
            })
        }
    )
import glob
import os
import re

from dagster import asset, MetadataValue, StaticPartitionsDefinition
from pyspark.sql import functions as F

from jornada_financas_pessoais.utils.cotahist_parser import parse_cotahist


SOURCE_PATH = "D:/Projetos/Jornada_financas_pessoais/data/raw"
BRONZE_PATH = "D:/Projetos/Jornada_financas_pessoais/data/bronze/raw_cotahist"

# Partições por ano (exemplo inicial)
cotahist_partitions = StaticPartitionsDefinition(
    [str(y) for y in range(2017, 2030)]
)


@asset(
    name="raw_cotahist",
    key_prefix=["bronze"],
    compute_kind="spark",
    description="Ingestão Bronze da cotação histórica da B3 (COTAHIST)",
    required_resource_keys={"spark"},
    partitions_def=cotahist_partitions,
)
def raw_cotahist(context):
    spark = context.resources.spark
    ano = context.partition_key  # chave da partição

    # 🔎 Busca apenas arquivos do ano da partição
    files = glob.glob(f"{SOURCE_PATH}/COTAHIST_A{ano}.TXT")

    if not files:
        context.log.warning(f"Nenhum arquivo encontrado para o ano {ano}")
        return MetadataValue.json(
            {"ano": ano, "registros": 0, "status": "sem_dados"}
        )

    context.log.info(f"{len(files)} arquivo(s) encontrados para {ano}")

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

    (
        df.write
        .format("delta")
        .mode("overwrite")               # idempotência
        .partitionBy("ano")              # partição física
        .option("overwriteSchema", "false")
        .save(BRONZE_PATH)
    )

    return MetadataValue.json({
        "ano": ano,
        "arquivos": [os.path.basename(f) for f in files],
        "registros": total,
        "destino": BRONZE_PATH
    })
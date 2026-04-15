from dagster import asset, AssetKey, MaterializeResult, MetadataValue, AutomationCondition
from pyspark.sql import functions as F
from pyspark.sql.types import DecimalType, IntegerType

from jornada_financas_pessoais.config.partitions import ANO_PARTITIONS
from jornada_financas_pessoais.config.paths import BRONZE_PATHS, SILVER_PATHS

BRONZE_PATH = BRONZE_PATHS["raw_cotahist"]
SILVER_PATH = SILVER_PATHS["stg_cotacao_historica"]


@asset(
    name="stg_cotacao_historica",
    key_prefix=["silver"],
    compute_kind="spark",
    description="Transforma a cotação histórica da Bronze para Silver",
    required_resource_keys={"spark"},
    partitions_def=ANO_PARTITIONS,
    deps=[AssetKey(["bronze", "raw_cotahist"])],
    op_tags={
        "dagster/max_retries": 3,
        "dagster/retry_delay": 60,
    },
    tags={
        "layer": "silver",
        "domain": "financeiro",
        "criticality": "high",
    },
    metadata={
        "owner": "squad-data-eng",
        "data_source": "RAW COTAHIST",
        "sla": "Dados do dia anterior disponíveis em D+1",
        "update_frequency": "Diário após fechamento do mercado (18h)",
        "data_classification": "Público",
        "retention_policy": "Permanente (dados históricos)",
   }
)
def stg_cotacao_historica(context):
    spark = context.resources.spark
    ano = context.partition_key

    context.log.info(f"Lendo Bronze {BRONZE_PATH} para o ano {ano}")

    df_bronze = (
        spark.read
        .format("delta")
        .load(BRONZE_PATH)      # Caminho base da tabela, sem a partição
        .where(f"ano_particao = {ano}")  # Filtra a partição usando predicado
    )

    # Verifica se há dados para o ano especificado
    if df_bronze.isEmpty():
        context.log.warning(f"Nenhum dado encontrado para o ano {ano}")
        return MaterializeResult(
            metadata={
                "processamento": MetadataValue.json({
                    "ano": ano,
                    "registros": 0,
                    "status": "sem dados"
                })
            }
        )
    
    total_registros = df_bronze.count()
    context.log.info(f"{total_registros} registros encontrados na Bronze para {ano}")

    # Transformações para Silver
    df_silver = df_bronze.select(
        F.col("tipo_registro").cast("string").alias("tipo_registro"),
        F.to_date(F.col("data_pregao"), "yyyyMMdd").alias("data_pregao"),
        F.col("codigo_bdi").cast("string").alias("codigo_bdi"),
        F.trim(F.col("codigo_negociacao")).alias("codigo_negociacao"),
        F.col("tipo_mercado").cast("string").alias("tipo_mercado"),
        F.trim(F.col("nome_resumido_empresa")).alias("nome_resumido_empresa"),
        F.trim(F.col("especificacao_papel")).alias("especificacao_papel"),
        F.col("prazo_dias_mercado").cast("string").alias("prazo_dias_mercado"),
        F.col("moeda_referencia").cast("string").alias("moeda_referencia"),
        (F.col("preco_abertura_papel") / 100).cast(DecimalType(11,2)).alias("preco_abertura_papel"),
        (F.col("preco_maximo_papel") / 100).cast(DecimalType(11,2)).alias("preco_maximo_papel"),
        (F.col("preco_minimo_papel") / 100).cast(DecimalType(11,2)).alias("preco_minimo_papel"),
        (F.col("preco_medio_papel") / 100).cast(DecimalType(11,2)).alias("preco_medio_papel"),
        (F.col("preco_ultimo_negocio") / 100).cast(DecimalType(11,2)).alias("preco_ultimo_negocio"),
        (F.col("preco_melhor_oferta_compra") / 100).cast(DecimalType(11,2)).alias("preco_melhor_oferta_compra"),
        (F.col("preco_melhor_oferta_venda") / 100).cast(DecimalType(11,2)).alias("preco_melhor_oferta_venda"),
        F.col("numero_negocios_efetuados").cast(IntegerType()).alias("numero_negocios_efetuados"),
        F.col("quantidade_total_titulos").cast(IntegerType()).alias("quantidade_total_titulos"),
        (F.col("volume_total_titulos") / 100).cast(DecimalType(16,2)).alias("volume_total_titulos"),
        (F.col("preco_exercicio_opcoes") / 100).cast(DecimalType(11,2)).alias("preco_exercicio_opcoes"),
        F.col("indicador_correcao_precos").cast("string").alias("indicador_correcao_precos"),
        F.to_date(F.col("data_vencimento_opcoes"), "yyyyMMdd").alias("data_vencimento_opcoes"),
        F.col("fator_cotacao_papel").cast("string").alias("fator_cotacao_papel"),
        (F.col("preco_exercicio_pontos") / 1000000).cast(DecimalType(7,6)).alias("preco_exercicio_pontos"),
        F.col("codigo_papel_sistema").cast("string").alias("codigo_papel_sistema"),
        F.col("numero_distribuicao_papel").cast("string").alias("numero_distribuicao_papel"),
        F.col("nome_arquivo_origem").cast("string").alias("nome_arquivo_origem"),
        F.lit(ano).alias("ano_particao"),  # coluna de partição
        F.current_timestamp().alias("criado_em")
    )

    # Gravação na Silver, garantindo partição por ano
    (
    df_silver.write.format("delta")
        .mode("overwrite")
        .option("replaceWhere", f"ano_particao = {ano}")
        .partitionBy("ano_particao")
        .option("overwriteSchema", "false")
        .save(SILVER_PATH)
    )    

    context.log.info(f"Silver gravada em: {SILVER_PATH} para o ano {ano}")

    return MaterializeResult(
        metadata={
            "processamento": MetadataValue.json({
                "ano": ano,
                "registros": total_registros,
                "destino": SILVER_PATH
            })
        }
    )

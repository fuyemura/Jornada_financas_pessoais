from dagster import asset, AssetKey, MaterializeResult, MetadataValue
from delta.tables import DeltaTable

from jornada_financas_pessoais.config.paths import SILVER_PATHS, GOLD_PATHS
from jornada_financas_pessoais.utils.ativo_financeiro import build_dim_ativo_financeiro

SILVER_PATH = SILVER_PATHS["stg_cotacao_historica"]
GOLD_PATH = GOLD_PATHS["dim_ativo_financeiro"]


@asset(
    name="dim_ativo_financeiro",
    key_prefix=["gold"],
    compute_kind="spark",
    description="Dimensão Ativo Financeiro (Star Schema) - SCD Type 1",
    required_resource_keys={"spark"},
    deps=[AssetKey(["silver", "stg_cotacao_historica"])]
)
def dim_ativo_financeiro(context):
    spark = context.resources.spark

    # Leitura Silver (toda a tabela, pois precisamos de todos os ativos para a dimensão)
    context.log.info(f"Lendo Silver {SILVER_PATH}")
    
    df_stg = spark.read.format("delta").load(SILVER_PATH)

    context.log.info(f"{df_stg.count()} registros encontrados na Silver")

    # Transformações para construir a dimensão
    df_dim = build_dim_ativo_financeiro(df_stg)

    delta_table = DeltaTable.forPath(spark, GOLD_PATH)

    #  Upsert Dimensão (SCD Type 1)
    (
        delta_table.alias("target")
        .merge(
            df_dim.alias("source"),
            "target.id_ativo_financeiro = source.id_ativo_financeiro"
        )
        .whenMatchedUpdate(
            condition="""
                coalesce(target.descricao_ativo, '') <> coalesce(source.descricao_ativo, '') OR
                coalesce(target.codigo_tipo_mercado, '') <> coalesce(source.codigo_tipo_mercado, '') OR
                coalesce(target.descricao_tipo_mercado, '') <> coalesce(source.descricao_tipo_mercado, '') OR
                coalesce(target.codigo_isin, '') <> coalesce(source.codigo_isin, '') OR
                coalesce(target.tipo_ativo, '') <> coalesce(source.tipo_ativo, '')
            """,
            set={
                "descricao_ativo": "source.descricao_ativo",
                "codigo_tipo_mercado": "source.codigo_tipo_mercado",
                "descricao_tipo_mercado": "source.descricao_tipo_mercado",
                "codigo_isin": "source.codigo_isin",
                "tipo_ativo": "source.tipo_ativo",
                "atualizado_em": "current_timestamp()"
            }
        )
        .whenNotMatchedInsert(values={
            "id_ativo_financeiro": "source.id_ativo_financeiro",
            "codigo_ativo": "source.codigo_ativo",
            "nome_empresa": "source.nome_empresa",
            "descricao_ativo": "source.descricao_ativo",
            "codigo_tipo_mercado": "source.codigo_tipo_mercado",
            "descricao_tipo_mercado": "source.descricao_tipo_mercado",
            "codigo_isin": "source.codigo_isin",
            "tipo_ativo": "source.tipo_ativo",
            "criado_em": "current_timestamp()",
            "atualizado_em": "null"
        })
        .execute()
    )

    metrics = delta_table.history(1).select("operationMetrics").collect()[0][0]

    return MaterializeResult(
        metadata={
            "processamento": MetadataValue.json({
                "inserted": int(metrics.get("numTargetRowsInserted", 0)),
                "updated": int(metrics.get("numTargetRowsUpdated", 0)),
                "destino": GOLD_PATH
            })
        }
    )

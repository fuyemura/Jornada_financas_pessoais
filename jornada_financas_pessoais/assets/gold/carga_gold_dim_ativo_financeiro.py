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
            "target.sk_ativo = source.sk_ativo"
        )
        .whenMatchedUpdate(
            condition="""
                coalesce(target.ds_ativo, '') <> coalesce(source.ds_ativo, '') OR
                coalesce(target.cd_tipo_mercado, '') <> coalesce(source.cd_tipo_mercado, '') OR
                coalesce(target.ds_tipo_mercado, '') <> coalesce(source.ds_tipo_mercado, '') OR
                coalesce(target.cd_isin, '') <> coalesce(source.cd_isin, '') OR
                coalesce(target.ds_tipo_ativo, '') <> coalesce(source.ds_tipo_ativo, '')
            """,
            set={
                "ds_ativo": "source.ds_ativo",
                "cd_tipo_mercado": "source.cd_tipo_mercado",
                "ds_tipo_mercado": "source.ds_tipo_mercado",
                "cd_isin": "source.cd_isin",
                "ds_tipo_ativo": "source.ds_tipo_ativo",
                "ts_atualizacao": "current_timestamp()"
            }
        )
        .whenNotMatchedInsert(values={
            "sk_ativo": "source.sk_ativo",
            "cd_ativo": "source.cd_ativo",
            "nm_empresa": "source.nm_empresa",
            "ds_ativo": "source.ds_ativo",
            "cd_tipo_mercado": "source.cd_tipo_mercado",
            "ds_tipo_mercado": "source.ds_tipo_mercado",
            "cd_isin": "source.cd_isin",
            "ds_tipo_ativo": "source.ds_tipo_ativo",
            "ts_insercao": "current_timestamp()",
            "ts_atualizacao": "null"
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

from pyspark.sql import functions as F, Window


def build_dim_ativo_financeiro(df_stg):
    # Apenas mercado à vista
    df = df_stg.filter(F.col("tp_mercado") == "010")

    window_spec = (
        Window
        .partitionBy("cd_negociacao", "tp_mercado")
        .orderBy(F.col("dt_pregao").desc())
    )

    df_latest = (
        df.withColumn("rn", F.row_number().over(window_spec))
          .filter(F.col("rn") == 1)
    )

    return df_latest.select(
        F.sha2(
            F.concat(F.col("cd_negociacao"), F.col("nm_empresa")),
            256
        ).alias("sk_ativo"),

        F.col("cd_negociacao").alias("cd_ativo"),
        F.col("nm_empresa"),
        F.col("ds_especificacao_papel").alias("ds_ativo"),
        F.col("tp_mercado").alias("cd_tipo_mercado"),

        F.when(F.col("tp_mercado") == "010", "VISTA")
         .when(F.col("tp_mercado") == "012", "EXERCÍCIO DE OPÇÕES DE COMPRA")
         .when(F.col("tp_mercado") == "013", "EXERCÍCIO DE OPÇÕES DE VENDA")
         .when(F.col("tp_mercado") == "017", "LEILÃO")
         .when(F.col("tp_mercado") == "020", "FRACIONÁRIO")
         .when(F.col("tp_mercado") == "030", "TERMO")
         .when(F.col("tp_mercado") == "050", "FUTURO COM RETENÇÃO DE GANHO")
         .when(F.col("tp_mercado") == "060", "FUTURO COM MOVIMENTAÇÃO CONTÍNUA")
         .when(F.col("tp_mercado") == "070", "OPÇÕES DE COMPRA")
         .when(F.col("tp_mercado") == "080", "OPÇÕES DE VENDA")
         .otherwise("DESCONHECIDO")
         .alias("ds_tipo_mercado"),

        F.lit(None).cast("string").alias("cd_isin"),
        F.lit("AÇÃO").alias("ds_tipo_ativo")
    )
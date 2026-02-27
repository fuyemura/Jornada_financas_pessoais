from pyspark.sql import functions as F, Window


def build_dim_ativo_financeiro(df_stg):
    # Apenas mercado à vista
    df = df_stg.filter(F.col("tipo_mercado") == "010")

    window_spec = (
        Window
        .partitionBy("codigo_negociacao", "tipo_mercado")
        .orderBy(F.col("data_pregao").desc())
    )

    df_latest = (
        df.withColumn("rn", F.row_number().over(window_spec))
          .filter(F.col("rn") == 1)
    )

    return df_latest.select(
        F.sha2(
            F.concat(F.col("codigo_negociacao"), F.col("nome_resumido_empresa")),
            256
        ).alias("id_ativo_financeiro"),

        F.col("codigo_negociacao").alias("codigo_ativo"),
        F.col("nome_resumido_empresa").alias("nome_empresa"),
        F.col("especificacao_papel").alias("descricao_ativo"),
        F.col("tipo_mercado").alias("codigo_tipo_mercado"),

        F.when(F.col("tipo_mercado") == "010", "VISTA")
         .when(F.col("tipo_mercado") == "012", "EXERCÍCIO DE OPÇÕES DE COMPRA")
         .when(F.col("tipo_mercado") == "013", "EXERCÍCIO DE OPÇÕES DE VENDA")
         .when(F.col("tipo_mercado") == "017", "LEILÃO")
         .when(F.col("tipo_mercado") == "020", "FRACIONÁRIO")
         .when(F.col("tipo_mercado") == "030", "TERMO")
         .when(F.col("tipo_mercado") == "050", "FUTURO COM RETENÇÃO DE GANHO")
         .when(F.col("tipo_mercado") == "060", "FUTURO COM MOVIMENTAÇÃO CONTÍNUA")
         .when(F.col("tipo_mercado") == "070", "OPÇÕES DE COMPRA")
         .when(F.col("tipo_mercado") == "080", "OPÇÕES DE VENDA")
         .otherwise("DESCONHECIDO")
         .alias("descricao_tipo_mercado"),

        F.lit(None).cast("string").alias("codigo_isin"),
        F.lit("AÇÃO").alias("tipo_ativo")
    )
from pyspark.sql import functions as F
from jornada_financas_pessoais.utils.cotahist_layout import COTAHIST_POSITIONS

def parse_cotahist(df_raw):
    ''' Extrai os campos do DataFrame raw de COTAHIST em formato fixo.'''
    df = df_raw.select(
        *[
            F.trim(
                F.substring(F.col("value"), start, end - start + 1)
            ).alias(field)
            for field, (start, end) in COTAHIST_POSITIONS.items()
        ],
        F.col("nome_arquivo"),
        F.col("ano")
    )

    return df.filter(F.col("tipo_registro") == "01")
BASE_DELTA_PATH = "D:/Projetos/Jornada_financas_pessoais/data"

SOURCE_PATHS = {
    "cotahist": f"{BASE_DELTA_PATH}/raw"
}

BRONZE_PATHS = {
    "raw_cotahist": f"{BASE_DELTA_PATH}/bronze/raw_cotahist"
}

SILVER_PATHS = {
    "stg_cotacao_historica": f"{BASE_DELTA_PATH}/silver/stg_cotacao_historica"
}

GOLD_PATHS = {
    "dim_ativo_financeiro": f"{BASE_DELTA_PATH}/gold/dim_ativo_financeiro"
}
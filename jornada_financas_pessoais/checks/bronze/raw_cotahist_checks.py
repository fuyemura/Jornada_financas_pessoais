import glob
import os

from dagster import AssetCheckSeverity, asset_check, AssetCheckResult
from pyspark.sql import functions as F

from jornada_financas_pessoais.config.paths import SOURCE_PATHS, BRONZE_PATHS
from jornada_financas_pessoais.contracts.cotahist_schema import EXPECTED_COLUMNS, SCHEMA_VERSION


SOURCE_PATH = SOURCE_PATHS["cotahist"]
BRONZE_PATH = BRONZE_PATHS["raw_cotahist"]

def carregar_raw_cotahist(context):
    """
    Leitura da tabela Delta Bronze COTAHIST.
    """
    ano = context.partition_key  # pega o ano da partição atual, ex: "2017"
    return (
        context.resources.spark.read
        .format("delta")
        .load(BRONZE_PATH)
        .filter(F.col("ano_particao") == ano)  # ajuste o nome da coluna de partição
    )


@asset_check(
    asset=["bronze", "raw_cotahist"],
    blocking=True,
    description="Verifica se o arquivo fonte existe para a partição",
)
def check_raw_cotahist_arquivo_fonte_existe(context):
    """
    Smoke test: Valida que o arquivo COTAHIST da B3 está presente no source.
    Se falhar, indica problema na fonte de dados ou no processo de coleta.
    """
    ano = context.partition_key
    files = glob.glob(f"{SOURCE_PATH}/COTAHIST_A{ano}.TXT")
    
    passed = len(files) > 0
    
    return AssetCheckResult(
        passed=passed,
        metadata={
            "ano": ano,
            "arquivos_encontrados": len(files),
            "path_verificado": f"{SOURCE_PATH}/COTAHIST_A{ano}.TXT",
            "arquivos": [os.path.basename(f) for f in files] if files else []
        },
        description=f"{'✓' if passed else '✗'} Arquivo fonte para {ano}"
    )


@asset_check(
    asset=["bronze", "raw_cotahist"],
    blocking=True,
    description="Valida que o schema bronze contém as colunas esperadas do contrato",
    required_resource_keys={"spark"},
)
def check_raw_cotahist_schema_contrato(context):
    """
    Smoke test: Verifica conformidade com o contrato de dados COTAHIST.
    Se falhar, indica mudança no formato da B3 ou problema no parse.
    """
    ano = context.partition_key

    try:
        df = carregar_raw_cotahist(context)
        colunas_presentes = set(df.columns)
        missing_columns = EXPECTED_COLUMNS - colunas_presentes
        extra_columns = colunas_presentes - EXPECTED_COLUMNS
        
        passed = len(missing_columns) == 0
        
        return AssetCheckResult(
            passed=passed,
            metadata={
                "ano": ano,
                "schema_version": SCHEMA_VERSION,
                "colunas_esperadas": len(EXPECTED_COLUMNS),
                "colunas_presentes": len(colunas_presentes),
                "colunas_faltando": list(missing_columns) if missing_columns else [],
                "colunas_extras": list(extra_columns) if extra_columns else [],
            },
            description=f"{'✓' if passed else '✗'} Schema conforme ao contrato v{SCHEMA_VERSION}"
        )
    except Exception as e:
        return AssetCheckResult(
            passed=False,
            metadata={
                "ano": ano,
                "erro": str(e)
            },
            description=f"✗ Erro ao validar schema da partição {ano}"
        )


@asset_check(
    asset=["bronze", "raw_cotahist"],
    description="Verifica sanidade básica: arquivo não está completamente vazio ou corrompido",
    required_resource_keys={"spark"},    
)
def check_raw_cotahist_sanidade_arquivo(context):
    """
    Smoke test: Valida tamanho mínimo razoável do arquivo.
    COTAHIST tem ~500k+ registros por ano. Menos de 1000 indica problema grave.
    """
    ano = context.partition_key
    REGISTROS_MINIMOS = 1000  # threshold conservador
    
    try:
        df = carregar_raw_cotahist(context)
        total = df.count()
        passed = total >= REGISTROS_MINIMOS
        
        return AssetCheckResult(
            passed=passed,
            metadata={
                "ano": ano,
                "total_registros": total,
                "minimo_esperado": REGISTROS_MINIMOS,
                "percentual_minimo": f"{(total/500000)*100:.2f}%" if total > 0 else "0%"
            },
            severity=AssetCheckSeverity.WARN if not passed else AssetCheckSeverity.ERROR,
            description=f"{'✓' if passed else '⚠'} Volume de dados: {total:,} registros"
        )
    except Exception as e:
        return AssetCheckResult(
            passed=False,
            metadata={
                "ano": ano,
                "erro": str(e)
            },
            description=f"✗ Erro ao verificar volume da partição {ano}"
        )
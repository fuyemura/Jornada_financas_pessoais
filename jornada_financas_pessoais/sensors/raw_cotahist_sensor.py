import glob
import os
import re

from dagster import (
    sensor,
    SensorEvaluationContext,
    RunRequest,
    SensorResult,
    SkipReason,
    AssetKey,
    asset_sensor,
)

from jornada_financas_pessoais.config.paths import SOURCE_PATHS

SOURCE_PATH = SOURCE_PATHS["cotahist"]
ARQUIVO_PATTERN = r"COTAHIST_A(\d{4})\.TXT"


@sensor(
    name="raw_cotahist_file_sensor",
    description="Monitora o diretório de origem e dispara raw_cotahist ao detectar novo arquivo COTAHIST",
    asset_selection=[AssetKey(["bronze", "raw_cotahist"])],
    minimum_interval_seconds=300,  # verifica a cada 5 minutos
)
def raw_cotahist_file_sensor(context: SensorEvaluationContext) -> SensorResult:
    # Cursor armazena os arquivos já processados (separados por vírgula)
    arquivos_ja_vistos: set[str] = set(
        context.cursor.split(",") if context.cursor else []
    )

    arquivos_encontrados = glob.glob(f"{SOURCE_PATH}/COTAHIST_A*.TXT")
    novos_run_requests = []
    arquivos_atuais = set()

    for caminho_arquivo in arquivos_encontrados:
        nome_arquivo = os.path.basename(caminho_arquivo)
        arquivos_atuais.add(nome_arquivo)

        if nome_arquivo in arquivos_ja_vistos:
            continue  # já foi processado anteriormente

        match = re.search(ARQUIVO_PATTERN, nome_arquivo)
        if not match:
            context.log.warning(f"Arquivo com nome inesperado ignorado: {nome_arquivo}")
            continue

        ano = match.group(1)
        context.log.info(f"Novo arquivo detectado: {nome_arquivo} → partição {ano}")

        novos_run_requests.append(
            RunRequest(
                run_key=nome_arquivo,       # garante idempotência: mesmo arquivo não dispara duas vezes
                partition_key=ano,
                tags={
                    "sensor": "cotahist_file_sensor",
                    "arquivo_origem": nome_arquivo,
                },
            )
        )

    if not novos_run_requests:
        return SensorResult(
            skip_reason=SkipReason(
                f"Nenhum arquivo novo encontrado em {SOURCE_PATH}"
            ),
            # Atualiza o cursor mesmo sem novos arquivos, para manter consistência
            cursor=",".join(arquivos_ja_vistos | arquivos_atuais),
        )

    # Atualiza o cursor com todos os arquivos vistos até agora
    novo_cursor = ",".join(arquivos_ja_vistos | arquivos_atuais)

    return SensorResult(
        run_requests=novos_run_requests,
        cursor=novo_cursor,
    )
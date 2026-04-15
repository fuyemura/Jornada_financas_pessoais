import glob
import hashlib
import os
import re

from dagster import (
    RunRequest,
    SensorEvaluationContext,
    SensorResult,
    SkipReason,
    sensor,
)

from jornada_financas_pessoais.config.paths import SOURCE_PATHS

SOURCE_PATH = SOURCE_PATHS["cotahist"]
ARQUIVO_PATTERN = r"COTAHIST_A(\d{4})\.TXT"


def hash_arquivo(caminho: str) -> str:
    with open(caminho, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:8]


@sensor(
    name="raw_cotahist_file_sensor",
    description="Monitora o diretório de origem e dispara raw_cotahist ao detectar novo arquivo COTAHIST",
    job_name="financas_pessoais_job",
    minimum_interval_seconds=300,  # verifica a cada 5 minutos
)
def raw_cotahist_file_sensor(context: SensorEvaluationContext) -> SensorResult:
    # Cursor armazena nome+hash dos arquivos já processados (separados por vírgula)
    arquivos_ja_vistos: set[str] = set(
        context.cursor.split(",") if context.cursor else []
    )

    arquivos_encontrados = glob.glob(f"{SOURCE_PATH}/COTAHIST_A*.TXT")
    novos_run_requests = []
    arquivos_atuais = set()

    for caminho_arquivo in arquivos_encontrados:
        nome_arquivo = os.path.basename(caminho_arquivo)
        hash_arq = hash_arquivo(caminho_arquivo)
        chave = f"{nome_arquivo}_{hash_arq}"  # chave única por nome + conteúdo

        arquivos_atuais.add(chave)  # cursor também usa nome + hash

        if chave in arquivos_ja_vistos:
            continue  # mesmo arquivo e mesmo conteúdo, ignora

        match = re.search(ARQUIVO_PATTERN, nome_arquivo)
        if not match:
            context.log.warning(f"Arquivo com nome inesperado ignorado: {nome_arquivo}")
            continue

        ano = match.group(1)
        context.log.info(f"Novo arquivo detectado: {nome_arquivo} (hash: {hash_arq}) → partição {ano}")

        novos_run_requests.append(
            RunRequest(
                run_key=chave,  # consistente com o cursor
                partition_key=ano,
                tags={
                    "sensor": "cotahist_file_sensor",
                    "arquivo_origem": nome_arquivo,
                },
            )
        )

    if not novos_run_requests:
        return SensorResult(
            skip_reason=SkipReason(f"Nenhum arquivo novo encontrado em {SOURCE_PATH}"),
            cursor=",".join(arquivos_ja_vistos | arquivos_atuais),
        )

    return SensorResult(
        run_requests=novos_run_requests,
        cursor=",".join(arquivos_ja_vistos | arquivos_atuais),
    )
from dagster import define_asset_job

financas_pessoais_job = define_asset_job(
    name="financas_pessoais_job",
    selection="*"
)
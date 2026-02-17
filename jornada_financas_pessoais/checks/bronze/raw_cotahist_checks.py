from dagster import asset_check, AssetCheckResult
from pyspark.sql import functions as F

@asset_check(asset=["bronze", "raw_cotahist"])
def raw_cotahist_nao_vazio(raw_cotahist):
    row_count = raw_cotahist.count()

    return AssetCheckResult(
        passed=row_count > 0,
        metadata={"row_count": row_count}
    )


@asset_check(asset=["bronze", "raw_cotahist"])
def raw_cotahist_sem_datas_nulas(raw_cotahist):
    null_count = raw_cotahist.filter(
        F.col("dt_pregao").isNull()
    ).count()

    return AssetCheckResult(
        passed=null_count == 0,
        metadata={"datas_nulas": null_count}
    )

from dagster import StaticPartitionsDefinition

ANO_PARTITIONS = StaticPartitionsDefinition(
    partition_keys=[str(ano) for ano in range(2017, 2027)]
)
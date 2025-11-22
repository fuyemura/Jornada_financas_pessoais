# spark_config.py
import os
from pyspark.sql import SparkSession

def init_spark(app_name="MeuApp"):
    """
    Inicializa Spark com Hive e Delta Lake persistente
    """
    # ===== CONFIGURAÇÃO DE DIRETÓRIOS =====
    BASE_DIR = "D:/Projetos/DataLake"
    WAREHOUSE_DIR = f"{BASE_DIR}/spark-warehouse"
    METASTORE_DIR = f"{BASE_DIR}/metastore_db"
    SCRATCH_DIR = f"{BASE_DIR}/hive_scratch"

    # Criar diretórios necessários
    for dir_path in [WAREHOUSE_DIR, SCRATCH_DIR]:
        os.makedirs(dir_path, exist_ok=True)

    # ===== CONFIGURAÇÃO DO HADOOP (Windows) =====
    os.environ['HADOOP_HOME'] = r'D:\hadoop'

    # ===== SPARK SESSION =====
    builder = (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")
        # Delta Lake
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        # Hive Local (persistente)
        .config("spark.sql.catalogImplementation", "hive")
        .config("spark.sql.warehouse.dir", f"file:///{WAREHOUSE_DIR}")
        .config("hive.metastore.warehouse.dir", f"file:///{WAREHOUSE_DIR}")
        .config(
            "javax.jdo.option.ConnectionURL",
            f"jdbc:derby:;databaseName={METASTORE_DIR};create=true"
        )
        # Corrige problemas no Windows
        .config("hive.exec.scratchdir", SCRATCH_DIR)
        .config("hive.metastore.schema.verification", "false")
        .config("hive.metastore.schema.verification.record.version", "false")
        .config("datanucleus.schema.autoCreateAll", "true")
        .enableHiveSupport()
    )

    from delta import configure_spark_with_delta_pip
    spark = configure_spark_with_delta_pip(builder).getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    print(f"\n✅ Spark {spark.version} iniciado com Hive local persistente!")
    print(f"📁 Warehouse: {WAREHOUSE_DIR}")
    print(f"📁 Metastore: {METASTORE_DIR}\n")
    
    return spark
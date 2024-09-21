# Imports
from pyspark.sql import SparkSession

# Create SparkSession
spark = SparkSession.builder \
           .appName('SparkByExamples.com') \
           .config("spark.jars",  r"D:\Spark\spark-3.5.0-bin-hadoop3\jars\mysql-connector-j-9.0.0.jar") \
           .getOrCreate()

# Create DataFrame 
columns = ["id", "name","age","gender"]
data = [(1, "James",30,"M"), (2, "Ann",40,"F"),
    (3, "Jeff",41,"M"),(4, "Jennifer",20,"F")]

sampleDF = spark.sparkContext.parallelize(data).toDF(columns)

# Write to MySQL Table
sampleDF.write \
  .format("jdbc") \
  .option("driver","com.mysql.cj.jdbc.Driver") \
  .option("url", "jdbc:mysql://localhost/bronze") \
  .option("dbtable", "employee") \
  .option("user", "financasp") \
  .option("password", "Financasp#321") \
  .save()
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import DoubleType, FloatType, LongType, StructType,StructField, StringType


S3_ENDPOINT = "http://minio:9000"
S3_ACCESS_KEY = "sparkaccesskey"
S3_SECRET_KEY = "sparksupersecretkey"

conf = (
    pyspark.SparkConf()
        .setAppName('app_name')
        .setMaster("spark://spark:7077")
  		#packages
        .set('spark.jars.packages', 'org.apache.iceberg:iceberg-spark-runtime-3.3_2.12:1.2.1,software.amazon.awssdk:url-connection-client:2.20.64,software.amazon.awssdk:bundle:2.20.64,org.postgresql:postgresql:42.6.0')
  		# S3 Config
        .set('spark.sql.extensions', 'org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions')
         .set('spark.sql.catalog.demo', 'org.apache.iceberg.spark.SparkCatalog')
        .set('spark.sql.catalog.demo.catalog-impl',  'org.apache.iceberg.jdbc.JdbcCatalog')
         .set('spark.sql.catalog.demo.uri', 'jdbc:postgresql://postgres:5432/iceberg?user=iceberg&password=iceberg')
         .set('spark.sql.catalog.demo.jdbc.user', 'iceberg')
         .set('spark.sql.catalog.demo.jdbc.password', 'iceberg')
         .set('spark.sql.catalog.demo.warehouse', 's3://warehouse')
         .set('spark.sql.catalog.demo.io-impl',    'org.apache.iceberg.aws.s3.S3FileIO')
         .set('spark.sql.catalog.demo.s3.endpoint', 'http://minio:9000')
         .set('spark.sql.catalog.spark_catalog', 'org.apache.iceberg.spark.SparkSessionCatalog')
         .set('spark.sql.defaultCatalog', 'demo')
         # spark.eventLog.enabled    true \
         # spark.eventLog.dir    /home/iceicedata/spark-events \
         # spark.history.fs.logDirectory     /home/iceicedata/spark-events \
         # .set('spark.sql.catalogImplementation', 'in-memory')
         .set('spark.executor.memory', '4g')
         .set('spark.driver.memory', '4g')
)

## Start Spark Session
spark = SparkSession.builder.config(conf=conf).getOrCreate()
print(f"Spark Jars: {spark.sparkContext._jsc.sc().listJars()}")

# spark.sql("""CREATE TABLE iceberg.my_table (
#     id bigint,
#     data string,
#     category string)
# USING iceberg
# OPTIONS (
#     'write.object-storage.enabled'=true, 
#     'write.data.path'='s3://warehouse')
# PARTITIONED BY (category);""")

# spark_df = spark.read.option("header", "true").csv("s3a://test/appl_stock.csv")

data = [{"Category": 'A', "ID": 1, "Value": 121.44, "Truth": True},
        {"Category": 'B', "ID": 2, "Value": 300.01, "Truth": False},
        {"Category": 'C', "ID": 3, "Value": 10.99, "Truth": None},
        {"Category": 'E', "ID": 4, "Value": 33.87, "Truth": True}
        ]

spark_df = spark.createDataFrame(data)
spark_df.writeTo("demo.my_table").createOrReplace()

# log_metric("spark_df.shape",spark_df.shape)

# iceberg_table_name = "wh.appl_stock_iceberg_table"

# #LOCATION 's3://warehouse/bronze/'

# spark_df.writeTo(iceberg_table_name).using("iceberg").createOrReplace()

# spark.sql("""CREATE DATABASE IF NOT EXISTS db LOCATION 's3://warehouse/db/'""")

# # spark.sql("""DROP TABLE IF EXISTS demo.table""")
# spark.sql("""CREATE TABLE demo.my_table (
# id bigint,
# data string,
# category string)
# USING iceberg
# LOCATION 's3://warehouse'""")

# spark_df.write.format("iceberg").mode("overwrite").save("demo.table")




# spark.sql("""INSERT INTO demo.table VALUES (1, 'a'), (2, 'b')""")
   

print("Spark Job Completed")

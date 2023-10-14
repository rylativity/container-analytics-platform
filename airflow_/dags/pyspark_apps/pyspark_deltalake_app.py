import pyspark
import os

AWS_ENDPOINT_URL = "http://minio:9000"
AWS_ACCESS_KEY_ID = "sparkaccesskey"
AWS_SECRET_ACCESS_KEY = "sparksupersecretkey"
S3_BUCKET = "warehouse"

# @task
# def write_deltalake_table():
conf = pyspark.SparkConf()
conf.setMaster("spark://spark:7077")
conf.set("spark.jars.packages", 'org.apache.hadoop:hadoop-aws:3.3.3,io.delta:delta-core_2.12:2.1.0')
# conf.set('spark.hadoop.fs.s3a.aws.credentials.provider', 'org.apache.hadoop.fs.s3a.AnonymousAWSCredentialsProvider')
conf.set('spark.hadoop.fs.s3a.endpoint', AWS_ENDPOINT_URL)
conf.set('spark.hadoop.fs.s3a.access.key', AWS_ACCESS_KEY_ID)
conf.set('spark.hadoop.fs.s3a.secret.key', AWS_SECRET_ACCESS_KEY)
conf.set('spark.hadoop.fs.s3a.path.style.access', "true")
conf.set("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
conf.set("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")


sc = pyspark.SparkContext(conf=conf)

spark = pyspark.sql.SparkSession(sc)

source_path = "s3a://test/appl_stock.csv"
    df = spark.read.option("header", "true").csv(source_path)


delta_table_name = "my_sales_data_from_spark_application"
write_path = f"s3a://{S3_BUCKET}/{delta_table_name}"
df.write.format("delta").save(write_path, mode="overwrite")


print("SUCCESSFULLY EXECUTED SPARK APPLICATION")

spark.stop()

# if __name__ == "__main__":
#     write_deltalake_table()
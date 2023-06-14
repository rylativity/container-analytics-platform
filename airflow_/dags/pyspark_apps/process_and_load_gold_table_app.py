import pyspark
import pyspark.sql.functions as F
import argparse

S3_ENDPOINT = "http://minio:9000"
S3_ACCESS_KEY = "sparkaccesskey"
S3_SECRET_KEY = "sparksupersecretkey"
S3_BUCKET = "warehouse"

parser = argparse.ArgumentParser()
parser.add_argument("--input-path", type=str)
parser.add_argument("--output-path", type=str)
args = vars(parser.parse_args())
print(f"Arguments: {args}")

## These args are passed in by the SparkSubmitOperator in Airflow
SILVER_TABLE_PATH = args["input_path"]
GOLD_TABLE_PATH = args["output_path"]

# @task
# def write_deltalake_table():
conf = pyspark.SparkConf()
conf.setMaster("spark://spark:7077")
conf.set("spark.jars.packages", 'org.apache.hadoop:hadoop-aws:3.3.2,io.delta:delta-core_2.12:2.1.0')
# conf.set('spark.hadoop.fs.s3a.aws.credentials.provider', 'org.apache.hadoop.fs.s3a.AnonymousAWSCredentialsProvider')
conf.set('spark.hadoop.fs.s3a.endpoint', S3_ENDPOINT)
conf.set('spark.hadoop.fs.s3a.access.key', S3_ACCESS_KEY)
conf.set('spark.hadoop.fs.s3a.secret.key', S3_SECRET_KEY)
conf.set('spark.hadoop.fs.s3a.path.style.access', "true")
conf.set("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
conf.set("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")


sc = pyspark.SparkContext(conf=conf)

spark = pyspark.sql.SparkSession(sc)

df = spark.read.format("delta").load(SILVER_TABLE_PATH)


## DATA AGGREGATION BY CUSTOMERID BELOW

df = df.withColumn("TransactionTotal", df.NumberOfItemsPurchased * df.CostPerItem)

df = df.groupBy("UserId")\
    .agg(
        F.sum("TransactionTotal").alias("total_spend"),
        F.avg("TransactionTotal").alias("avg_spend_per_transaction"),
        F.sum("NumberOfItemsPurchased").alias("total_items_purchased"),
        F.countDistinct("ItemCode").alias("distinct_items_purchased")
    )

df.write.format("delta").save(GOLD_TABLE_PATH, mode="overwrite")


print("SUCCESSFULLY EXECUTED SPARK APPLICATION")

spark.stop()

# if __name__ == "__main__":
#     write_deltalake_table()
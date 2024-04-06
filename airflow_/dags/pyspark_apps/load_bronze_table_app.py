import pyspark
import argparse

AWS_ENDPOINT_URL = "http://minio:9000"
AWS_ACCESS_KEY_ID = "sparkaccesskey"
AWS_SECRET_ACCESS_KEY = "sparksupersecretkey"
S3_BUCKET = "warehouse"

parser = argparse.ArgumentParser()
parser.add_argument("--input-path", type=str)
parser.add_argument("--output-path", type=str)
args = vars(parser.parse_args())
print(f"Arguments: {args}")

## These args are passed in by the SparkSubmitOperator in Airflow
SOURCE_CSV_TABLE_PATH = args["input_path"]
BRONZE_TABLE_PATH = args["output_path"]

# @task
# def write_deltalake_table():
conf = pyspark.SparkConf()
conf.setMaster("spark://spark:7077")
conf.set("spark.jars.packages", 'org.apache.hadoop:hadoop-aws:3.3.4,io.delta:delta-spark_2.12:3.1.0')
# conf.set('spark.hadoop.fs.s3a.aws.credentials.provider', 'org.apache.hadoop.fs.s3a.AnonymousAWSCredentialsProvider')
conf.set('spark.hadoop.fs.s3a.endpoint', AWS_ENDPOINT_URL)
conf.set('spark.hadoop.fs.s3a.access.key', AWS_ACCESS_KEY_ID)
conf.set('spark.hadoop.fs.s3a.secret.key', AWS_SECRET_ACCESS_KEY)
conf.set('spark.hadoop.fs.s3a.path.style.access', "true")
conf.set("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
conf.set("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")


sc = pyspark.SparkContext(conf=conf)

spark = pyspark.sql.SparkSession(sc)

df = spark.read.option("header", "true").csv(SOURCE_CSV_TABLE_PATH)


df.write.format("delta").save(BRONZE_TABLE_PATH, mode="overwrite")


print("SUCCESSFULLY EXECUTED SPARK APPLICATION")

spark.stop()

# if __name__ == "__main__":
#     write_deltalake_table()
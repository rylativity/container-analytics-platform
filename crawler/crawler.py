from io import BytesIO
import logging
import os
from typing import Dict, List

import boto3
import pyhive
import pyarrow.parquet as pq
import pyarrow as pa

log = logging.getLogger(__name__)

S3_ENDPOINT_URL = os.environ.get("CRAWLER_S3_ENDPOINT_URL")
S3_BUCKET = os.environ.get("CRAWLER_S3_BUCKET")
S3_ACCESS_KEY = os.environ.get("CRAWLER_S3_ACCESS_KEY")
S3_SECRET_KEY = os.environ.get("CRAWLER_S3_SECRET_KEY")
DEBUG = os.environ.get('DEBUG')
# if DEBUG:
#     log.setLevel("DEBUG")
log.setLevel("DEBUG")

## Mapper to map parquet types to Trino types
parquet_trino_type_map = {
    pa.int8(): "BIGINT",
    pa.int16(): "BIGINT",
    pa.int32(): "BIGINT",
    pa.int64(): "BIGINT",
    pa.float16(): "DOUBLE",
    pa.float32(): "DOUBLE",
    pa.float64(): "DOUBLE",
    pa.timestamp('ns'): "TIMESTAMP",
    pa.timestamp('us'): "TIMESTAMP",
    pa.timestamp('ms'): "TIMESTAMP",
    pa.timestamp('s'): "TIMESTAMP",
    pa.binary(): "BOOLEAN",
    pa.string(): "VARCHAR"
}

class Crawler:

    def __init__(self, access_key=S3_ACCESS_KEY, secret_key=S3_SECRET_KEY, endpoint_url=S3_ENDPOINT_URL) -> None:
        log.debug(f"Attempting to initialize Crawler using Access Key ID {access_key}")
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            endpoint_url=endpoint_url
        )
    
    def crawl_bucket(self, bucket = S3_BUCKET):
        log.error(f"Crawling bucket {bucket}")
        
        ### Identify S3 Prefixes and Object keys
        paginator = self.s3_client.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=bucket)
        all_prefixes: List[str] = []
        all_keys: List[str] = []
        for page in page_iterator:
            contents = page["Contents"]
            keys = [obj["Key"] for obj in contents]
            all_keys.extend(keys)
            prefixes = ["/".join(k.split("/")[:-1]) for k in keys]
            all_prefixes.extend(prefixes)
        all_prefixes = list(set(all_prefixes))   
        print("Found Keys:", all_keys)
        print("Found Prefixes:", all_prefixes)

        # Identify parquet files and extract their schemas
        keys: List[str] = [k for k in all_keys if k.endswith((".parq",".parquet"))]        
        pq_schemas: List = []
        for f in keys:
            content = BytesIO(self.s3_client.get_object(Bucket=bucket, Key=f)["Body"].read())
            schema = pq.read_schema(content)
            pq_schemas.append(dict(zip(schema.names, schema.types)))

        print("Found Parquet Files... \n")
        for i in range(len(keys)):
            print("File:", keys[i])
            print("Schema:", pq_schemas[i], "\n")
        print(pq_schemas[1] == pq_schemas[0])
        
        return dict(zip(keys, pq_schemas))

        # Create SQL Statements to Register Hive Tables through Trino

    def generate_create_table_statements(schema_config: Dict[str, Dict[str, pa.DataType]]):
        obj_keys = schema_config.keys()
        schemas = schema_config.values()

        hive_statements: List[str] = []
        for i, schema in enumerate(schemas):
            prefix_segments = obj_keys[i].split("/")[:-1]
            table_name = obj_keys[i].split("/")[-1]
            schema_name = "".join([segment[0].upper() + segment[1:].lower() for segment in prefix_segments])
            hive_statements.append(f"""
                CREATE SCHEMA IF NOT EXISTS {schema_name};
                DROP TABLE
            """)
        


        
        
            

if __name__ == "__main__":
    c = Crawler(access_key="crawleraccesskey", secret_key="crawlersupersecretkey", endpoint_url="http://localhost:9000")
    c.crawl_bucket(bucket="test")
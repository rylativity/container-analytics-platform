import os

import boto3
import pyhive

import logging

log = logging.getLogger(__name__)

S3_ENDPOINT_URL = os.environ.get("CRAWLER_S3_ENDPOINT_URL")
S3_BUCKET = os.environ.get("CRAWLER_S3_BUCKET")
S3_ACCESS_KEY = os.environ.get("CRAWLER_S3_ACCESS_KEY")
S3_SECRET_KEY = os.environ.get("CRAWLER_S3_SECRET_KEY")
DEBUG = os.environ.get('DEBUG')
# if DEBUG:
#     log.setLevel("DEBUG")
log.setLevel("DEBUG")

class Crawler:

    def __init__(self, access_key=S3_ACCESS_KEY, secret_key=S3_SECRET_KEY) -> None:
        log.debug(f"Attempting to initialize Crawler using Access Key ID {access_key}")
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
    
    def crawl_bucket(self, bucket = S3_BUCKET):
        log.info(f"Crawling bucket {bucket}")
        
        paginator = self.s3_client.get_paginator('list_objects_v2')

        page_iterator = paginator.paginate(Bucket=bucket)
        all_prefixes = []
        for page in page_iterator:
            contents = page["Contents"]
            keys =  [obj["Key"] for obj in contents]
            prefixes = ["/".join(k.split("/")[:-1]) for k in keys]
            ...
            



        

if __name__ == "__main__":
    c = Crawler()
    res = c.crawl()
    print(res)
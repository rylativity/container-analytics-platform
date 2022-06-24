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
        
        paginator = self.s3_client.get_paginator('list_objects_v2')

        page_iterator = paginator.paginate(Bucket=bucket)
        all_prefixes = []
        all_keys = []
        for page in page_iterator:
            contents = page["Contents"]
            keys = [obj["Key"] for obj in contents]
            all_keys.append(keys)
            prefixes = ["/".join(k.split("/")[:-1]) for k in keys]
            all_prefixes.extend(prefixes)
        
        all_prefixes = list(set(all_prefixes))
        print(all_keys)
        print(all_prefixes)
            

if __name__ == "__main__":
    c = Crawler(access_key="crawleraccesskey", secret_key="crawlersupersecretkey", endpoint_url="http://localhost:9000")
    c.crawl_bucket(bucket="test")
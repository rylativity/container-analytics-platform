#!/bin/bash
docker-compose run --entrypoint '/bin/bash -c' --rm aws \
     'aws s3 cp --recursive --no-sign-request --exclude "*" --include "yellow_tripdata_*2022-*.parquet" "s3://nyc-tlc/trip data/" ~/data && \
          aws --endpoint-url http://minio:9000 s3 cp --recursive ~/data s3://test/taxi --no-sign-request'
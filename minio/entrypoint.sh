#!/bin/bash
set -euxo pipefail
until curl -s -f -o /dev/null "http://minio:9000/minio/health/ready"
do
  sleep 5
done
for f in /docker-entrypoint-initdb.d/*.sh; do
  bash "$f"
done

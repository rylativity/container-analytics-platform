#!/bin/bash
set -euxo pipefail
until mc alias set myminio http://minio:9000 minio minio123; mc ready myminio
do
  sleep 5
done
for f in /docker-entrypoint-initdb.d/*.sh; do
  bash "$f"
done

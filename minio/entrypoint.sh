#!/bin/bash
set -exuo pipefail
for f in /docker-entrypoint-initdb.d/*.sh; do
  bash "$f"
done

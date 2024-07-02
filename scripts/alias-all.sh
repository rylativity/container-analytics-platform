#!/bin/bash

## Run 'source scripts/alias-all.sh to set alias'

ALIAS=cap-compose

alias $ALIAS='docker compose -f docker-compose.yml -f docker-compose-datahub.yml -f docker-compose-spark.yml -f docker-compose-superset.yml -f docker-compose-airflow.yml'

echo "All services docker-compose-*.yml merged and aliased to $ALIAS. (e.g. invoke like '$ALIAS up -d')"

docker-compose exec trino trino --execute "$(cat ./dataload_scripts/trino_commands.txt)"

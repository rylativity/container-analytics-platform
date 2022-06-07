# Hive Standalone Metastore with Postgres Backend and Minio (S3 Compatible Object Storage) in Docker

This project contains all files needed to set up and test a Hive Standalone Metastore.  The docker-compose.yml file defines three services: a Postgres container (backend for Hive), a Hive Metastore Container, and a Minio Container (which you can use as a drop-in replacement for AWS S3) for testing the Hive metastore on an Object Store.

## Setup
- Run `docker-compose up metastore-init` (this command will fail after the DB has been initialized once)
- After the metastore initialization in complete (it should say "exited with code 0"), run `docker-compose up -d metastore`
- To view logging output, run `docker-compose logs -f`

***

## Explanation of Services in the Docker-Compose.yml
**TODO**

### Minio
You can access the minio console at http://localhost:9090. You can create buckets and upload files through the Minio Console.  

Buckets in the Minio Object Store are programatically accessable at http://localhost:9000.  Any operations you would performa against an S3 bucket can be performed against the Minio Object Store.  

You can use the AWS CLI v2 to interact with a Minio bucket as if it were an S3 bucket by specifying the endpoint URL.  For example, to list the objects in a **public** Minio bucket called `test-bucket`, you would run:
`aws --endpoint-url http://localhost:9000 s3 ls s3://test-bucket/ --no-sign-request`

To add some sample data to Minio, run `./dataload_scripts/load_taxidata_to_minio.sh`, which will download the NYC Yellow Cab trip data in parquet format and upload it to the Minio "test" bucket (which is created by the 'createbuckets' container defined in docker-compose.yml)

### Trino
Once you have sample data in Minio, you can register schemas and tables in Hive using the Trino CLI.  If you loaded the sample NYC Yellow Cab trip data to Minio (as described above), you can run `./dataload_scripts/register_trino_hive_tables.sh`, which will execute the Trino commands to create a new schema and add a table with the external Minio data location as the source.

***

## Roadmap
- [x] Initalize Minio (by creating bucket and adding taxi Parquet data - https://registry.opendata.aws/nyc-tlc-trip-records-pds/) 
- [x] Initialize Trino (by creating a hive table from Parquet taxi data in Minio)
- [ ] Resolve bug in Standalone Metastore (NoSuchObjectException 'hive.<schema>.<table>' no such table) when attempting to create hive table
- [ ] Update README.md with explanation of services
- [ ] Update README.md with instructions for using example data & init scripts

## Tips & Troubleshooting
 - Stick with bucketnames that use only lowercase letters and no special characters.  
# Container Analytics Platform

This project contains all configuration files needed to set up a modern, distributed, containerized analytics environment, allowing you to query data where it lies (in this case, in a S3 object store, in ElasticSearch, and in MongoDB). The docker-compose.yml file defines the following services: a Postgres container (backend for Hive Metastore), a Hive Metastore Container, a Minio Container (which you can use as a drop-in replacement for AWS S3) for testing the Hive metastore on an Object Store, a Trino container for querying data out of S3(Minio) using the Hive Metastore, and the four services that make up Superset for dashboarding data through Trino.  There are also examples and usage instructions for interacting with the various services.

The docker-compose.yml also defines an ElasticSearch service and a MongoDB service (both of which are commented out).  If you wish to use ElasticSearch and/or MongoDB, uncomment the relevant lines in the docker-compose.yml (including their volume definitions at the bottom of the docker-compose.yml), and modify the relevant filenames in trino/catalog to remove ".template" (e.g. elasticsearch.properties.template -> elasticsearch.properties).  Trino will read any files in the trino/catalog folder that ends with ".properties".

## Pre-Requisites
- Working installations of Docker and docker-compose (if you do not have either of these installed, Google the installation instructions, follow the official installation instructions for your operating system, and then return here to continue)
- Experience with Docker & docker-compose (if you do not have experience with Docker or docker-compose, it would help to get some experience by following the official Docker quick-start guides; while not required, it will definitely be easier to understand this project if you understand Docker and docker-compose)
- A high level understanding of Trino (or Presto), Hive Standalone Metastore, and S3 or Minio (if you don't know about any of these, spend a few minutes researching them and then return here to continue)

## Setup
- Run `docker-compose up -d` (This will bring up the containers, initalize the metastore postgres database, create a 'test' bucket with public permissions in Minio, and create Minio service account access-keys/secrets for Spark and Trino)
- Once the containers have started, navigate to Jupyter Lab at http://localhost:8888. Run the included notebook to write some Delta Lake tables. This is also a great way to learn a bit about PySpark & Delta Lake. (All code should run as-is). This essentially simulates placing data in an S3 bucket (e.g. as the result of an ETL job)
- Navigate to the Superset UI at http://localhost:8088 and log in with the username and password below (or in the docker-compose.yml). Connect Superset to Trino (and by extension the Delta Lake tables in Minio which Trino can read like SQL tables) by selecting Data > Databases > +Database > Select Trino as DB Type > Set SQLAlchemy URI = 'trino://trino@trino:8080/delta'; also make sure to expose the database in SQL Lab and check the boxes next to "Allow CREATE TABLE AS", "Allow CREATE VIEW AS", and "Allow DML" under the 'Advanced' options.
- Navigate to SQL Lab in the Superset UI, select the new Trino database connection from the appropriate dropdown menu, and run the SQL commands listed below under the "Superset" section of this README. These commands show you how to read Delta Lake tables through Trino & Superset without having to specify the schema ahead of time!

## Service Endpoints
- Jupyter Lab - http://localhost:8888
- Spark UI - http://localhost:8090
- Minio UI - http://localhost:9090 (user: minio, password: minio123)
- Trino UI - http://localhost:8080 (user: *any*)
- Superset UI - http://localhost:8088 (user: admin, password: admin)
- Trino Shell - `docker-compose exec trino trino` (Use this to run SQL commands against data in Minio)
*Any host ports can be changed in the docker-compose.yml*

***

## Explanation and Usage of Services in the Docker-Compose.yml

### Jupyter
##### DOCUMENTATION TODO #####

### Spark/Spark-Worker
##### DOCUMENTATION TODO #####

### Delta Lake
##### DOCUMENTATION TODO #####

### Minio
Minio is an S3-Compatible object store that can be run locally or on any cloud platform.  In other words, Minio is a free, drop-in replacement for S3 that you have full control over.  In addition to countless other uses, Minio is a great standin for S3 while doing local development.

Credentials for Minio (including the admin username, password, and service account credentials) can be found in the docker-compose.yml file.

You can access the minio console at http://localhost:9090. You can create buckets and upload files through the Minio Console.  

Buckets in the Minio Object Store are programatically accessable at http://localhost:9000.  Any operations you would perform against an S3 bucket can be performed against the Minio Object Store.  

For example, you can use the AWS CLI v2 to interact with a Minio bucket as if it were an S3 bucket by specifying the endpoint URL.  For example, to list the objects in a **public** Minio bucket called `test`, you would run:
`aws --endpoint-url http://localhost:9000 s3 ls s3://test/ --no-sign-request`.



***

### Trino
Trino is a distributed query engine that can connect to many different datasources including SQL databases, document databases (e.g. MongoDB), and even data files sitting in S3 (by leveraging a Hive Standalone Metastore).  Trino will even allow you to execute queries that pull in data from different datasources (e.g. you can query data from S3 and left join in a SQL table in a single query).

Once you have Delta Lake data in Minio (S3), you can read Delta Tables directly from Trino through the trino shell (or through Superset SQL Lab; see setup steps at top of README for instructions for adding sample data and connecting Superset).

Example Commands - https://trino.io/docs/current/connector/hive.html#examples


https://trino.io/docs/current/connector/hive.html#examples

***

### Metastore (Hive Standalone Metastore)
The Hive Metastore allows us to project a table-like structure onto data sitting in Minio (or S3).  We connect the Hive Metastore to Presto, and then use SQL commands issued to Presto to "create" tables out of data (JSON, CSV, ORC, PARQUET, etc...) in S3 and query the data.

The Hive Metastore does not need to be interacted with directly.  Presto's Hive Connector is used to configure the connection with Presto (see the file presto/catalog/hive.properties), and Presto handles updating the Hive Metastore.

If you are interested in seeing the contents of the Hive Metastore, you can use `docker-compose exec metastore bash` to open a terminal in the Hive Metastore container.  The actual Metastore data is stored at /etc/hive_metastore inside the container (Note: you will need to use `ls -a` to list the contents of folders in /etc/hive_metastore, since many of the files are "hidden")

***

### Superset
Apache Superset is arguably one of the best BI tools available, ignoring the fact that it is completely free and open-source.  In this project, Superset serves as a front-end for Trino.  You can use its SQL Lab Editor to write and execute queries against any datasource registered in Trino, and you can use it to create visuals and dashboards.

Superset is accessible at http://localhost:8088 (Username: admin, Password: admin) once you have gone through the setup steps.  To connect Superset to Trino using Superset's Trino connector, login to the Superset UI and add Trino as a Database (select "Data" > "Databases" > "+Database" > "Trino", the SQLALCHEMY URI should be "trino://trino@trino:8080/hive" - the hostname/URL "trino" is simply the docker service name of trino as defined in the docker-compose.yml).

Once connected, Superset's SQL Lab Editor can be used as a frontend for the Trino query engine (which in turn can be used to query Delta Lake tables directly from Minio(S3)).

A cloud object store bucket called 'test' is automatically created for you in Minio (navigate to http://localhost:9090 after you've started the containers and log in with the username and password from the docker-compose.yml)

Run the SQL commands below  in the Superset SQL Lab Editor to have Trino automatically read Delta Lake (without having to provide schema ahead of time). DO NOT REPLACE THE "dummy bigint" column definition in the CREATE TABLE statment - Trino will ignore that column definition and read the schema from Delta:
```
DROP SCHEMA IF EXISTS delta.my_schema;

CREATE SCHEMA delta.my_schema
WITH (location = 's3a://test/');

CREATE TABLE delta.my_schema.my_table (
  dummy bigint
)
WITH (
  location = 's3a://test/appl_stock_delta_table'
);

SELECT * FROM delta.my_schema.my_table;

-- Drop tables and schemas if desired (YOU MUST STILL MANUALLY DELETE THE DATA FROM S3)
-- DROP TABLE delta.my_schema.my_table;
-- DROP SCHEMA delta.my_schema.my_table;
```

## Roadmap
- [x] Initalize Minio (by creating bucket and adding taxi Parquet data - https://registry.opendata.aws/nyc-tlc-trip-records-pds/) 
- [x] Initialize Trino (by creating a hive table from Parquet taxi data in Minio)
- [x] Resolve bug in Standalone Metastore (NoSuchObjectException 'hive.<schema>.<table>' no such table) when attempting to create hive table
- [ ] Add ClickHouse server and examples (https://clickhouse.com/docs/en/tutorial/, https://hub.docker.com/r/clickhouse/clickhouse-server/#!)
- [ ] Add example notebook using delta-rs python bindings to interact with delta lake
- [ ] Document a demo walkthrough of steps to do when first starting with project
- [ ] Develop frontend Vue application to display services in central location
- [ ] Add reverse proxy (preferably Traefik or NginX) for services
- [ ] Update README.md with explanation of services and instructions for including datahub, spark, and superset in startup
- [ ] Split up docker-compose to create a set of base services (with lower resource usage) and optional add-ons
- [ ] Add detailed usage guides for services
  - [ ] Jupyter
  - [ ] Spark
  - [ ] Delta Lake
  - [ ] DataHub
  - [ ] Add Screenshots
- [ ] Update README.md with instructions for using example data & init scripts
- [x] Add Superset to Project for Data Exploration
- [x] Add Datahub Data Catalog (implemented on branch `datahub`. Is fairly resource intensive, and often requires multiple runs of `docker-compoe up mysql-setup elasticsearch-setup` before `docker-compose up -d`)
- [ ] Build out datahub automated startup process
- [x] Add Dynamic FastAPI & Swagger Docs based on Trino Hive tables (created as separate project - https://github.com/rylativity/autoapi)
- [ ] Add Minio/S3 schema crawler to crawl buckets and create schemas that can be used to create Hive tables
- [x] Add Spark+Jupyter & Delta containers and examples

## Troubleshooting
- While you can have multiple Trino catalog connectors of type hive and delta, schema names must be globally unique (i.e. a schema name defined in a hive connection cannot be used in a delta connection)

# Container Analytics Platform

### Note: This README is slightly out-of-date as changes to this repo are relatively frequent. Updates to README are in progress.

While I recommend reading the entire README, you can skip to the Setup Instructions below if you know what you are doing and just want to get started.

This project contains all configuration files needed to set up am entirely open-source, cloud-native, distributed, containerized, data-lakehouse analytics environment. The services used in this project were specifically selected for functionality and compatibility with one another. The combination of object storage (Minio), an open data-lakehouse data storage format (Delta Lake), support for multiple query engines (e.g. Trino, Spark, etc...), and additional metadata layer services/capabilities (e.g. data-catalogging, metadata management, etc...) are what make this a "data lakehouse" architecture.

The project is designed to be modular and allow you to spin up the specific services that you are interested in learning or building on top of. It also contains examples to help you get started with common tasks like loading and processing data, orchestrating pipelines, tracking data qualilty, using various services APIs, creating dashboards, and catalogging data assets.

The services included in this project are listed below. Some of the services have initialization scripts, configuration files, data, or other assets that the containers need access to upon startup. These files are stored in folders with names that correspond to the service that uses them. There is also a "data" folder that contains sample data used by some of the examples provided in this project.

### Base Services
The docker-compose.yml defines the following services (and their supporting services, e.g. init containers):
- Jupyter Lab - Python notebook editor and interactive python environment.
- Postgres Database - Transactional application database used by various other services in the environment.
- Minio - Object store and central storage for data lakehouse data. Drop-in replacement for AWS S3.
- Trino - Distributed query engine. Allows us to query Delta Lake data in files in S3 (Minio) with low latency as if it were a SQL database. Suitable for serving real-time analytics use-cases.
- Hive Metastore Service - (NOT HIVE) The metastore service that Trino uses to manage metadata for Delta Lake tables.
- Redis - Cache and message broker used by various other services in the environment.

### Auxiliary Services
The following services are each defined in their own .yml files, with filenames corresponding to the service defined within them.
- Airflow (docker-compose-airflow.yml) - Orchestration of data pipelines (or anything else you might want to orchestrate).
- Spark (docker-compose-spark.yml) - Distibuted data processing and query engine.
- Superset (docker-compose-superset.yml) - Dashboarding and reporting.
- Datahub (docker-compose-datahub.yml) - Data cataloging (including datasets, dashboards, machine-learning models, and more)


## Pre-Requisites
- Working installations of Docker and docker-compose (if you do not have either of these installed, Google the installation instructions, follow the official installation instructions for your operating system, and then return here to continue)
- Experience with Docker & docker-compose (if you do not have experience with Docker or docker-compose, it would help to get some experience by following the official Docker quick-start guides; while not required, it will definitely be easier to understand this project if you understand Docker and docker-compose)
- A basic understanding of (or willingness to learn) the services you want to use
- The base services can comfortably be run on 2 vCPU and 8gb RAM, while all services combined can comfortably be run on 8 vCPU and 32gb RAM (I have not measured specific numbers, but can confirm from my own experience. Your mileage may vary depending on your circumstances.)

## Setup Instructions
The project is separated into a set of base services, defined in the docker-compose.yml file, and auxiliary services, defined in the other docker-compose-*.yml files. You must run the base services as the auxiliary services have dependencies on some of those base services, and you can run any or all of the auxiliary services alongside the base services.

### Steps
- Decide which services you want to spin up. I recommend starting with the base services and using the notebooks in the Jupyter container to get comfortable.
- Bring up the relevant services
  - If you are just using the base services, run `docker compose up -d` (This will bring up the containers, initalize the metastore postgres database, create a 'test' bucket with public permissions in Minio, and create Minio service account access-keys/secrets for the other services)
  - If you want to use auxiliary services, run `docker compose -f docker-compose.yml [-f docker-compose-<service>.yml] up -d`. For example, to use the base services, Superset, and Spark, you would run `docker compose -f docker-compose.yml -f docker-compose-spark.yml -f docker-compose-superset.yml up -d`. I **strongly** recommend aliasing your docker compose command if using any auxiliary services to make subsequent `docker compose` commands easier. For example, `alias cap-compose='docker compose -f docker-compose.yml -f docker-compose-spark.yml -f docker-compose-superset.yml'`. Now I could run `cap-compose logs -f` to get logs from all deployed services instead of having to type out all the filenames each time.

## Service Endpoints

Once the services have started, the services can be accessed at the following endpoints.
- Jupyter Lab - http://localhost:8888
- Spark UI - http://localhost:8090
- Minio UI - http://localhost:9090 (user: minio, password: minio123)
- Trino UI - http://localhost:8080 (user: *any*)
- Superset UI - http://localhost:8088 (user: admin, password: admin)
- Trino Shell - `docker-compose exec trino trino` (Use this to run SQL commands against data in Minio)

*Any host ports can be changed in the docker-compose.yml or the relevant .yml file for the relevant service*

***

## Explanation and Usage of Services in the Docker-Compose.yml

### Jupyter
##### DOCUMENTATION TODO #####

Once the containers have started, navigate to Jupyter Lab at http://localhost:8888. Run the sample notebooks. This is a great way to learn a bit about PySpark & Delta Lake. (All code should run as-is).

### Spark/Spark-Worker
##### DOCUMENTATION TODO #####

### Delta Lake
##### DOCUMENTATION TODO #####

### Nginx
##### DOCUMENTATION TODO #####

### CloudBeaver
##### DOCUMENTATION TODO #####

### DataHub
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
Consider running the Pyspark notebook in the Jupyter service or the pipelines in the Airflow service to load data before using Superset.

Apache Superset is arguably one of the best BI tools available, ignoring the fact that it is completely free and open-source.  In this project, Superset serves as a front-end for Trino.  You can use its SQL Lab Editor to write and execute queries against any datasource registered in Trino, and you can use it to create visuals and dashboards.

Navigate to the Superset UI at http://localhost:8088 and log in with the username and password below (or in the docker-compose.yml). Connect Superset to Trino (and by extension the Delta Lake tables in Minio which Trino can read like SQL tables) by selecting Data > Databases > +Database > Select Trino as DB Type > Set SQLAlchemy URI = 'trino://trino@trino:8080/delta'; also make sure to expose the database in SQL Lab and check the boxes next to "Allow CREATE TABLE AS", "Allow CREATE VIEW AS", and "Allow DML" under the 'Advanced' options.

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

### Features and Services
- [ ] Nginx Configuration for all Services (with 301 redirect for services that don't support base url)
- [ ] Develop frontend Vue application to display services in central location
- [ ] Add Minio/S3 schema crawler to crawl buckets and create schemas that can be used to create Hive tables
- [ ] Develop datahub init process
- [ ] Develop CloudBeaver init process (https://dbeaver.com/docs/cloudbeaver/Configuring-server-datasources/)
- [x] Initalize Minio
- [x] Initialize Trino (by creating a hive table from Parquet taxi data in Minio)
- [x] Resolve bug in Standalone Metastore (NoSuchObjectException 'hive.<schema>.<table>' no such table) when attempting to create hive table
- [x] Add example notebook using delta-rs python bindings to interact with delta lake
- [x] Split up docker-compose to create a set of base services (with lower resource usage) and optional add-ons
- [x] Add Superset to Project for Data Exploration
- [x] Add Datahub Data Catalog (implemented on branch `datahub`. Is fairly resource intensive, and often requires multiple runs of `docker-compoe up mysql-setup elasticsearch-setup` before `docker-compose up -d`)
- [x] Add Dynamic FastAPI & Swagger Docs based on Trino Hive tables (created as separate project - https://github.com/rylativity/autoapi)
- [x] Add Spark+Jupyter & Delta containers and examples

### Documentation
- [ ] Document a demo walkthrough of steps to do when first starting with project
- [ ] Update README.md with explanation of services and instructions for including datahub, spark, and superset in startup- [ ] Add detailed usage guides for services
  - [ ] Jupyter
  - [ ] CloudBeaver
  - [ ] Spark
  - [ ] Delta Lake
  - [ ] DataHub
  - [ ] Nginx
  - [ ] Add Screenshots
- [ ] Update README.md with instructions for using example data & init scripts


## Troubleshooting
- While you can have multiple Trino catalog connectors of type hive and delta, schema names must be globally unique (i.e. a schema name defined in a hive connection cannot be used in a delta connection)

FROM quay.io/minio/mc:RELEASE.2024-05-03T11-21-07Z

COPY docker-entrypoint-initdb.d/ /docker-entrypoint-initdb.d/

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]

FROM quay.io/minio/mc

COPY docker-entrypoint-initdb.d/ /docker-entrypoint-initdb.d/

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]

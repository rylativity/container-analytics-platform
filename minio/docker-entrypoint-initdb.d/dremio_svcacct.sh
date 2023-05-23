#!/bin/bash
sleep 3;

/usr/bin/mc alias set myminio http://minio:9000 minio minio123;
/usr/bin/mc admin user svcacct add --access-key 'dremioaccesskey' --secret-key 'dremiosupersecretkey' myminio minio;
exit 0;

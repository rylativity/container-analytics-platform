#!/bin/bash
sleep 3;

/usr/bin/mc alias set myminio http://minio:9000 minio minio123;
/usr/bin/mc mb myminio/test;
/usr/bin/mc policy set public myminio/test;
/usr/bin/mc admin user svcacct add --access-key 'jupyteraccesskey' --secret-key 'jupytersupersecretkey' myminio minio;
exit 0;
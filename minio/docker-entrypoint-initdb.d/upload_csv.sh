#!/bin/bash
sleep 3;

/usr/bin/mc alias set myminio http://minio:9000 minio minio123;
/usr/bin/mc mb --ignore-existing myminio/test;
/usr/bin/mc policy set public myminio/test;
/usr/bin/mc cp /data/appl_stock.csv myminio/test/appl_stock.csv;
/usr/bin/mc cp /data/transaction_data.csv myminio/test/transaction_data.csv;
exit 0;
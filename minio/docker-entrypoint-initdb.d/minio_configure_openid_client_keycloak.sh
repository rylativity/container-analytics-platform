#!/bin/bash
set -euxo pipefail;
/usr/bin/mc alias set myminio http://minio:9000 minio minio123;
/usr/bin/mc idp openid add myminio keycloak \
   client_id=minio \
   client_secret=secretvalue \
   config_url="http://keycloak:8080/realms/analytics/.well-known/openid-configuration" \
   display_name="Minio" \
   scopes="openid,email,policy" \
   redirect_uri_dynamic="on"

/usr/bin/mc admin service restart myminio;
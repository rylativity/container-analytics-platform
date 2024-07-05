#!/bin/bash
set -euxo pipefail
source ./get-admin-token.sh
curl --location --request GET 'http://localhost:8123/admin/realms' \
   --header "Authorization: Bearer $TOKEN"

#!/bin/bash
set -euxo pipefail
source ./get-admin-token.sh
curl --location --request POST 'http://localhost:8123/admin/realms' \
--header "Authorization: Bearer $TOKEN" \
--header 'Content-Type: application/json' \
--data-raw '{
    "id": "analytics",
    "realm": "analytics",
    "displayName": "Analytics",
    "enabled": true,
    "sslRequired": "external",
    "registrationAllowed": true,
    "loginWithEmailAllowed": true,
    "duplicateEmailsAllowed": false,
    "resetPasswordAllowed": false,
    "editUsernameAllowed": false,
    "bruteForceProtected": true
  }'


#!/bin/bash
export TOKEN=`curl --location --request POST 'http://localhost:8123/realms/master/protocol/openid-connect/token' --header 'Content-Type: application/x-www-form-urlencoded' --data-urlencode 'client_id=admin-cli' --data-urlencode 'username=admin' --data-urlencode 'password=admin' --data-urlencode 'grant_type=password' | jq -r '.access_token'`
echo $TOKEN


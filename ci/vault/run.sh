#!/bin/sh
set -m

if [ -z "$VAULT_DEV_ROOT_TOKEN_ID" ]; then
    export VAULT_DEV_ROOT_TOKEN_ID=testtoken
fi
if [ -z "$VAULT_DEV_LISTEN_ADDRESS" ]; then
    export VAULT_DEV_LISTEN_ADDRESS=0.0.0.0:8200
fi

export VAULT_ADDR=http://0.0.0.0:8200
export VAULT_TOKEN=$VAULT_DEV_ROOT_TOKEN_ID

vault server -dev -dev-listen-address="$VAULT_DEV_LISTEN_ADDRESS" -dev-root-token-id="$VAULT_TOKEN" &
sleep 1 && \
vault secrets enable database && \
vault write database/config/database \
    plugin_name="postgresql-database-plugin" \
    connection_url="postgresql://{{username}}:{{password}}@127.0.0.1:5555/fastapi-boilerplate?sslmode=disable" \
    allowed_roles="testrole2" \
    username="fastapi-boilerplate" \
    password="fastapi-boilerplate" && \
vault write database/roles/testrole2 \
    db_name=database \
    creation_statements="CREATE ROLE \"testrole2\" WITH LOGIN PASSWORD '{{password}}'; \
        GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"fastapi-boilerplate\";" \
    default_ttl="1h" \
    max_ttl="24h"
wait
#!/usr/bin/env bash

set -u

ENV_VAR_FILE=".env"

# Load env vars to use with envsubst
export $(grep -v '^#' ${ENV_VAR_FILE} | xargs)

# Make sure necessary directories are created
mkdir -p ${MYSQL_DATA_DIR} ${MYSQL_CONF_DIR} ${MYSQL_ENTRYPOINT_DIR}

# Set all variables using the config env var file .env
envsubst < mysql/script.sql.example > "${MYSQL_ENTRYPOINT_DIR}/script.sql"

# Start docker containers
docker-compose up -d 

# TODO: wait until mysql is up and import csv base book list

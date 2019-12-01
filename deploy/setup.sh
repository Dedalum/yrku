#!/usr/bin/env bash

set -u

ENV_VAR_FILE=".env"

# Load env vars to use with envsubst
export $(grep -v '^#' ${ENV_VAR_FILE} | xargs)

# Make sure necessary directories are created
mkdir -p ${MYSQL_DATA_DIR} ${MYSQL_CONF_DIR} ${MYSQL_ENTRYPOINT_DIR}
mkdir -p ${NLP_RECOMMEND_DATA_DIR} ${NLP_RECOMMEND_CONF_DIR}
mkdir -p ${WEBAPP_DIR} ${WEBAPP_CONF_DIR}
mkdir -p ${NGINX_DIR} ${NGINX_CONFD_DIR} ${NGINX_LOG_DIR}

# Set all variables using the config env var file .env
envsubst < ./mysql/script.sql.example > "${MYSQL_ENTRYPOINT_DIR}/script.sql"
envsubst < ./nlpservices/recommend/config.ini.example > "${NLP_RECOMMEND_CONF_DIR}/config.ini"
envsubst < ./webapp/.env.example > "${WEBAPP_DIR}/.env"
envsubst < ./webapp/config/nlp_api.php.example > "${WEBAPP_CONF_DIR}/nlp_api.php"

# nginx uses variables with '$' sign which collides with our own variables
# we avoid that by passing to envsubst the list of variables to replace
vars_to_replace=$(grep -P "\\$\\{[A-Z_]*\\}" nginx/conf.d/webapp.conf.example -o)
envsubst "$vars_to_replace" < ./nginx/conf.d/webapp.conf.example > "${NGINX_CONFD_DIR}/webapp.conf"



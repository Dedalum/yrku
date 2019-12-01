#!/usr/bin/env bash

set -u
set -e

function print_err () {
    echo -e "\e[31mERR: ${1}\e[0m"
    return 1
}

function print_info () {
    echo -e "\e[32mINFO: ${1}\e[0m"
}

function print_help () {
    echo -e "Deploy the project, running the commands in the order given bellow.
Usage: ${0} <cmd> [param]
Commands:
    pre_setup       setup configs and start DB
    prepare_db      import training data to the DB
    start_all       start all services: nlrecommend, nginx, webapp
    setup_webapp    setup webapp: migrate tables   
"
}

function pre_setup () {
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
    
    docker-compose up -d db
}

function prepare_db () {
    ./mysql_mngt.sh import_csv    
}

function start_all () {
    docker-compose up -d nlprecommend webapp nginx
}

function setup_webapp () {
    if [[ -z $WEBAPP_KEY ]]; then
        print_err "Webapp app key is not defined. Add the private key to the webbap/.env config file"
    fi

    print_info "Migrating..."
    docker-compose exec webapp bash -c "php artisan migrate"
}


function main() {
    if [[ ! -f .env ]]; then
        print_err ".env missing in current dir"
        exit 1
    fi

    ENV_VAR_FILE=".env"
    
    # Load env vars
    export $(grep -v '^#' ${ENV_VAR_FILE} | xargs)


    if [[ -z "${1:-}" ]]; then
        print_help
        exit 0
    fi

    local choice=${1}

    case ${choice} in
    "pre_setup")
        pre_setup
        print_info "Starting DB and setting configs"
        ;;
    "prepare_db")
        prepare_db
        print_info "Importing training data to DB"
        ;;
    "start_all")
        start_all
        print_info "Starting other services"
        ;;
    "setup_webapp")
        setup_webapp
        print_info "Setting up webapp"
        ;;
    *)
        print_err "Bad command"
        print_help
        exit 1
        ;;
    esac
}

main "${@}"

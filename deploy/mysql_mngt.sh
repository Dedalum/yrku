#!/usr/bin/env bash

set -u

function print_err () {
    echo -e "\e[31mERR: ${1}\e[0m"
}

function print_info () {
    echo -e "\e[32mINFO: ${1}\e[0m"
}

function print_help () {
    echo -e "Usage: ${0} <cmd>
Commands:
    clean_table         truncate table ${MYSQL_TABLE_NAME}
    import_csv          import CSV book file ${BOOKS_CSV} in the 
                        table ${MYSQL_TABLE_NAME}
"
}

function clean_table() {
    docker exec $DB_CONTAINER_NAME sh -c "mysql -u $MYSQL_ADMIN_USER \
        -p$MYSQL_ADMIN_PASSWORD \
        -e \"TRUNCATE TABLE ${MYSQL_TABLE_NAME}\" \
        $MYSQL_DB_NAME"

    if [[ $? -ne 0 ]]; then
        print_err "failed to clean DB table ${MYSQL_TABLE_NAME}"
        exit 1
    fi
}

function import_csv() {    
    cp "${BOOKS_CSV}" "${MYSQL_ENTRYPOINT_DIR}/."
    if [[ $? -ne 0 ]]; then
        print_err "failed to copy ${BOOKS_CSV} to ${MYSQL_ENTRYPOINT_DIR}"
        exit 1
    fi

    docker exec ${DB_CONTAINER_NAME} sh -c "mysql -u ${MYSQL_ADMIN_USER} \
        -p${MYSQL_ADMIN_PASSWORD} \
        --local-infile \
        -e \"LOAD DATA LOCAL INFILE '${CONTAINER_BOOKS_CSV_PATH}' \
        INTO TABLE ${MYSQL_TABLE_NAME} \
        FIELDS TERMINATED BY ',' \
        ENCLOSED BY '\\\"' \
        LINES TERMINATED BY '\\n' \" \
        ${MYSQL_DB_NAME}"

    if [[ $? -ne 0 ]]; then
        print_err "failed to load CSV into DB"
        exit 1
    fi
    
    rm "${MYSQL_ENTRYPOINT_DIR}/${BOOKS_CSV}" 
}

function select_all_books() {
    docker exec $DB_CONTAINER_NAME sh -c "mysql -u $MYSQL_ADMIN_USER \
        -p$MYSQL_ADMIN_PASSWORD \
        -e \"SELECT * from ${MYSQL_TABLE_NAME}\" \
        $MYSQL_DB_NAME"
}

function main() {
    if [[ ! -f .env ]]; then
        print_err ".env missing in current dir"
        exit 1
    fi

    source .env

    if [[ -z "${1:-}" ]]; then
        print_help
        exit 0
    fi

    local choice=${1}

    case ${choice} in
    "clean_table")
        clean_table
        print_info "table truncated"
        ;;
    "import_csv")
        import_csv
        print_info "CSV file imported"
        ;;
    "select_all_books")
        select_all_books
        ;;
    *)
        print_err "Bad command"
        print_help
        exit 1
        ;;
    esac
}

main "${@}"

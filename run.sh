#!/usr/bin/env bash

export PYTHONPATH="$PYTHONPATH:src/database/:src/message/:src/auth/:src/user/"
if [[ $1 == "local" ]]; then
    export USERS_DB_ADDRESS="127.0.0.1"
    export USERS_DB_PORT="5004"
    uvicorn --port 5001 --reload src.auth.auth-service:app &
    uvicorn --port 5002 --reload src.user.user-service:app &
    uvicorn --port 5003 --reload src.message.message-service:app &
    docker compose --file ./src/database/init/docker-compose.yaml up
    pkill -TERM -P $$
elif [[ $1 == "openapi" ]]; then
    ./openapi/gen-docs.py src/*/*-service.py --out-dir ./openapi/
else
    export COMPOSE_BAKE=true
    docker compose down --remove-orphans
    docker compose build
    docker compose up
fi

#!/usr/bin/env bash

export PYTHONPATH="$PYTHONPATH:src/database/:src/message/:src/auth/:src/user/"
if [[ $1 == "local" ]]; then
    uvicorn --port 5001 --reload src.auth.auth-service:app &
    uvicorn --port 5002 --reload src.user.user-service:app &
    uvicorn --port 5003 --reload src.message.message-service:app
elif [[ $1 == "openapi" ]]; then
    ./openapi/gen-docs.py src/*/*-service.py --out-dir ./openapi/
else
    COMPOSE_BAKE=true docker compose build
    COMPOSE_BAKE=true docker compose up
fi

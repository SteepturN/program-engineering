#!/usr/bin/env bash

if [[ $# -ge 1 ]]; then
    uvicorn --port 5001 --reload auth-service:app &
    uvicorn --port 5002 --reload user-service:app &
    uvicorn --port 5003 --reload message-service:app
else
    COMPOSE_BAKE=true docker compose build
    COMPOSE_BAKE=true docker compose up
fi

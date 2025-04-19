FROM python:3.12.9-bullseye
WORKDIR /app

# https://stackoverflow.com/a/67281822
COPY ./src src/

RUN python -m pip install -r src/requirements.txt

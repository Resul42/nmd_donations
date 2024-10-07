FROM python:alpine3.20

USER root
WORKDIR /app
COPY . . 

RUN pip install -r requirements.txt

ENTRYPOINT [ "sh", "docker-entrypoint.sh" ]

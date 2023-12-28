FROM python:3.9-slim-bullseye
RUN apt-get update && apt install -y nginx curl
COPY default /etc/nginx/site-available/default
WORKDIR /app
COPY . .
RUN pip install -r requirment.text
RUN curl -L -O https://artifacts.elastic.co/downloads/apm-server/apm-server-7.17.15-amd64.deb
USER root
RUN dpkg -i apm-server-7.17.15-amd64.deb
RUN mv apm-server.yml /etc/apm-server/apm-server.yml
RUN chmod 755 /etc/apm-server/apm-server.yml
RUN service apm-server start
CMD gunicorn myproject:app -c gunicorn_config.py

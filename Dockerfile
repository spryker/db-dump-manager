FROM ubuntu:20.04

RUN apt-get update -y
RUN apt-get install -y python3
RUN apt-get install -y pip
RUN apt-get install -y libpq-dev python-dev

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata
RUN apt-get install -y mysql-server

COPY requirements.txt .

RUN pip install psycopg2-binary
RUN pip install -r requirements.txt

WORKDIR db-dump-manager

VOLUME /db-dump-manager

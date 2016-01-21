FROM debian:jessie

MAINTAINER Orestis Ioannou <orestis@oioannou.com>

ENV DEBIAN_FRONTEND noninteractive

# PACKAGES
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y \
    python3 \
    python3-pip \
    python3-setuptools \
    postgresql-9.4 \
    python3-psycopg2 \
    python3-nose \
    python3-nose2-cov

# dev tools
RUN apt-get install -y lynx vim

# SETUP

### DEBSOURCES
RUN apt-get install -y git
RUN mkdir /etc/bookpit

ENV PYTHONPATH /opt/bookpit

### POSTGRES
# needs to run postgres to create a user
# the root superuser is here to permit to run the tests suite
USER postgres
RUN /etc/init.d/postgresql start &&\
    psql --command "CREATE USER docker WITH SUPERUSER PASSWORD 'docker';" &&\
    psql --command "CREATE USER root WITH SUPERUSER;" &&\
    createdb -O docker bookpit &&\
    true

USER root

ADD requirements.txt .
RUN pip3 install -r requirements.txt

EXPOSE 80


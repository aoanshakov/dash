FROM debian:buster

RUN apt-get update -y
RUN apt-get upgrade -y

RUN apt-get install -y wget gnupg
RUN wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | apt-key add -

RUN echo "deb http://repo.mongodb.org/apt/debian buster/mongodb-org/5.0 main" \
    | tee /etc/apt/sources.list.d/mongodb-org-5.0.list

RUN apt-get update -y

RUN apt-get install -y \
    systemd \
    openssl \
    gnupg2 \
    ca-certificates \
    lsb-release \
    git \
    curl \
    python3 \
    python3-pip \
    python3-venv \
    mongodb-org

RUN echo "deb http://nginx.org/packages/debian `lsb_release -cs` nginx" \
    | tee /etc/apt/sources.list.d/nginx.list

RUN curl -fsSL https://nginx.org/keys/nginx_signing.key | apt-key add -
RUN apt-get update -y
RUN apt-get install nginx

RUN curl -sL https://deb.nodesource.com/setup_13.x | bash -
RUN apt-get install -y nodejs
RUN curl -L https://npmjs.org/install.sh | sh

ADD run-server /usr/local/bin/run-server

ENTRYPOINT bash

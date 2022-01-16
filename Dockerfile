FROM debian:buster

COPY install-debian-packages /
RUN install-debian-packages

ENTRYPOINT bash

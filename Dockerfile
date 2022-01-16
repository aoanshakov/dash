FROM debian:buster

COPY sumerians-to-greek/work_folder/install-debian-packages /
RUN /install-debian-packages

ENTRYPOINT bash

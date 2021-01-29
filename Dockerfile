FROM python:3.5.2

EXPOSE 27017
EXPOSE 5000

RUN mkdir /opt/tatools/
COPY . /opt/tatools/

WORKDIR /opt/tatools/


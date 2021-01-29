FROM python

MAINTAINER JDH

USER root

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
RUN echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-3.0.list

RUN apt-get install -y nodejs
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y mongodb-org=3.0.1 mongodb-org-server=3.0.1 mongodb-org-shell=3.0.1 mongodb-org-mongos=3.0.1 mongodb-org-tools=3.0.1

EXPOSE 27017
EXPOSE 5000

RUN mkdir /opt/tatools/
COPY . /opt/tatools/

WORKDIR /opt/tatools/



ENTRYPOINT [ "/entrypoint.sh"]
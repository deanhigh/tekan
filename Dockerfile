FROM python

MAINTAINER JDH

USER root

#RUN apt-get install python-pandas


#scipy python-matplotlib ipython python-pandas sympy python-nose atlas-devel

RUN mkdir /opt/tatools

COPY . /opt/tatools/

WORKDIR /opt/tatools

RUN pip install -r requirements.txt


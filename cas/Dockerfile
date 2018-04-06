FROM alpine:3.6
MAINTAINER btimby@smartfile.com

RUN apk --update add git python3 uwsgi-python3

ADD . /app

WORKDIR /app
RUN rm Makefile Dockerfile start
RUN pip3 install -r requirements.txt

RUN  rm -rf /var/cache/apk/*

ADD start /start

ENTRYPOINT ["/bin/sh"]

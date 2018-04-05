FROM alpine:3.6
MAINTAINER btimby@smartfile.com

RUN apk --update add python3 uwsgi-python3

ADD . /app
ADD start /start

WORKDIR /app
RUN rm Makefile Dockerfile start
RUN pip3 install -r requirements.txt

RUN  rm -rf /var/cache/apk/*

ENTRYPOINT ["/bin/sh"]

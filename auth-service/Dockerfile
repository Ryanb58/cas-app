FROM alpine:3.6
MAINTAINER btimby@smartfile.com

RUN apk --update add git python3 python3-dev uwsgi-python3 build-base libxml2 \
                     libxslt libxml2-dev libxslt-dev

ADD . /app

WORKDIR /app
RUN rm Makefile Dockerfile start
RUN pip3 install -r requirements.txt

RUN apk del --purge build-base python3-dev libxml2-dev libxslt-dev && \
    rm -rf /var/cache/apk/*

ADD start /start

ENTRYPOINT ["/bin/sh"]

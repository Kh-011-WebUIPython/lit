FROM ubuntu:14.04
LABEL maintainer="Max Krivich"
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install uwsgi
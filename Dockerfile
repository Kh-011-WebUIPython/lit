FROM python:3
LABEL maintainer="Max Krivich"
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
RUN pip install uwsgi
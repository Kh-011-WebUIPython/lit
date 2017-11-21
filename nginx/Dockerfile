FROM nginx:latest
LABEL maintainer="Max Krivich"
COPY nginx.conf /etc/nginx/nginx.conf
COPY my_nginx.conf /etc/nginx/sites-available/
RUN mkdir -p /etc/nginx/sites-enabled/\
    && ln -s /etc/nginx/sites-available/my_nginx.conf /etc/nginx/sites-enabled/
RUN mkdir -p /app/.well-known
RUN apt update
RUN apt install letsencrypt
CMD ["nginx", "-g", "daemon off;"]
RUN letsencrypt certonly --webroot -w /app/ -d litvcs.win -d www.litvcs.win

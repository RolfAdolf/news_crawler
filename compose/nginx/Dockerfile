FROM nginx:1.19.7

RUN rm /etc/nginx/conf.d/default.conf
COPY ./compose/nginx/nginx.conf /etc/nginx/conf.d/
COPY ./compose/nginx/config.conf /etc/nginx/nginx.conf
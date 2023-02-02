FROM nginx

COPY ./proxy.conf /etc/nginx/proxy.conf
COPY ./nginx.conf /etc/nginx/nginx.conf

COPY ./default.conf /etc/nginx/conf.d/default.conf

FROM node:13.3-alpine as generator
WORKDIR /app/src
COPY ./frontend/package.json /app/src
RUN npm install
COPY ./frontend /app/src

FROM generator as builder
WORKDIR /app/src
RUN npm run build

FROM nginx:1.13.6
RUN apt-get update && apt-get install \
    python3 \
    gcc \
    python3-dev \
    virtualenv -y 
RUN python3 -m virtualenv --python=/usr/bin/python3 venv
COPY requirements.txt .
RUN . venv/bin/activate && pip install -r requirements.txt
COPY --from=builder /app/src/dist /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.site.conf /etc/nginx/conf.d/nginx.site.conf
COPY wsgi.ini /usr/share/wsgi/wsgi.ini
COPY backend backend
COPY docker_start.sh docker_start.sh
RUN chmod +x docker_start.sh
EXPOSE 80

# CMD . venv/bin/activate && uwsgi --ini /usr/share/wsgi/wsgi.ini && exec nginx -g 'daemon off;'
CMD /bin/bash docker_start.sh

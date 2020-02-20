FROM node:13.3-alpine as generator
WORKDIR /app/src
COPY ./frontend/package.json /app/src
RUN npm install
COPY ./frontend /app/src

FROM generator as builder
WORKDIR /app/src
RUN npm run build

FROM nginx:1.13.6
WORKDIR /usr/share/nginx/html
COPY --from=builder /app/src/dist .
EXPOSE 80

FROM node:16-alpine as build

ARG VUE_APP_PROTOCOL
ENV VUE_APP_PROTOCOL $VUE_APP_PROTOCOL

WORKDIR /app
COPY . .
RUN env
RUN npm install && npm run build

FROM lucaslorentz/caddy-docker-proxy:2.8-alpine
COPY --from=build /app/dist /var/www


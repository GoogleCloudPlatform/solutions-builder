FROM node:16.17.0-alpine as builder
ARG API_DOMAIN
ARG FIREBASE_API_KEY
ARG FIREBASE_APP_ID
ARG PROJECT_ID
WORKDIR /app
COPY . .
RUN npm install --save-exact
RUN npm run build

FROM nginx:1.17.10-alpine
RUN rm -rf /usr/share/nginx/html/* && rm -rf /etc/nginx/nginx.conf
COPY --from=builder /app/nginx.conf /etc/nginx/nginx.conf
COPY --from=builder /app/dist/frontend_angular /usr/share/nginx/html

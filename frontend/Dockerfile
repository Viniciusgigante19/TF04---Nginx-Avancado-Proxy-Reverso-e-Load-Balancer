FROM node:alpine

WORKDIR /app

COPY . .

RUN npm install -g http-server

EXPOSE 3000

CMD ["http-server", ".", "-p", "3000", "-a", "0.0.0.0", "-c-1", "--no-listing"]
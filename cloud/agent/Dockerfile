FROM node:latest
RUN mkdir /app
WORKDIR /app
EXPOSE 1337 1338

COPY ./package.json .
RUN npm install

COPY ./src /app/src

CMD ["npm", "start"]
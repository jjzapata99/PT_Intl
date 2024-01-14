FROM node:lts

WORKDIR /app

COPY . .

RUN npm install --force


EXPOSE 3000

ENTRYPOINT ["npm", "run", "dev"]
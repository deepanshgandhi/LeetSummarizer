FROM node:alpine

WORKDIR /usr/src/app
copy package*.json ./
RUN npm install

COPY . .
EXPOSE 3000
CMD ["npm", "start"]
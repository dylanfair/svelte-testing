FROM node:16-alpine AS build

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install

COPY . ./

#EXPOSE 5173

#ENV HOST=0.0.0.0

RUN npm run build

#WORKDIR dist

FROM nginx:1.19-alpine
COPY --from=build /usr/src/app/dist /usr/share/nginx/html
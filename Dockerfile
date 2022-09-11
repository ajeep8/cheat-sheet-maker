FROM node:14-alpine as cheatsheet
LABEL authors="Ajeep"

WORKDIR /app

COPY . .

#RUN npm -v; npm config set registry https://registry.npm.taobao.org; npm install \
RUN npm -v; npm install \
  && cd client; npm install \
  && npm run build \
  && rm -rf *.js *.json node_modules public src /app/.git /app/.github /app/screenshots
  # && chown -R node.node /cheat-sheet-maker

COPY . /app
#COPY _env /app/.env
CMD [ "npm", "run", "dev" ]

FROM node:14-alpine AS cheatsheet_product
WORKDIR /app
COPY --from=cheatsheet /app /app
CMD [ "npm", "run", "start", "--production" ]



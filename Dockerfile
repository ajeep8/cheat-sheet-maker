FROM node:14-alpine as cheatsheet
LABEL authors="Ajeep"

WORKDIR /app

COPY . .

RUN npm -v; npm install \
  && cd client; npm install \
  && npm run build \
  && rm -rf *.js *.json node_modules public src
  # && chown -R node.node /cheat-sheet-maker

COPY . /app
#COPY _env /app/.env

#CMD [ "npm", "run", "dev" ]

#FROM node:14-alpine AS cheatsheet_product
#COPY --from=cheatsheet /cheat-sheet-maker /cheat-sheet-maker
CMD [ "npm", "run", "start", "--production" ]

FROM node:lts-bookworm as builder

WORKDIR /home/node/app
COPY ./package*json .
RUN npm ci --omit=dev
COPY . .
RUN npm run build

FROM node:lts-bookworm

WORKDIR /home/node/app
COPY --from=builder /home/node/app/.output /home/node/app
EXPOSE 3000

CMD ["node", "server/index.mjs"]

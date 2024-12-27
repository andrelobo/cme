# Arquivo: ./frontend/Dockerfile
FROM node:20

WORKDIR /app

COPY package.json yarn.lock ./
RUN yarn install

COPY . .

# Use "--host 0.0.0.0" para permitir conexões externas
CMD ["yarn", "dev", "--host", "0.0.0.0"]

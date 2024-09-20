#docker build --pull --rm -f "Dockerfile.ali" -t cheatsheet:v0.3 .
docker build --target cheatsheet -t cheatsheet:dev .
docker build --target cheatsheet_product -t cheatsheet:prod .


#!/bin/sh
#docker build --pull --rm --build-arg https_proxy=http://10.222.1.1:7890 -f "Dockerfile" --target aryabase -t aryabase:v0.3 .
#docker build --pull --rm -f "Dockerfile" --target aryabase -t aryabase:v0.3 .

#docker build --pull --rm --build-arg https_proxy=http://10.222.1.1:7890 -f "Dockerfile" --target arya -t arya:v0.3 .
docker build --pull --rm -f "Dockerfile.ali" -t cheatsheet:v0.3 .


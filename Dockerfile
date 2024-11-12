FROM --platform=linux/amd64 python:3.9-slim-bullseye 

ARG AwsSecretKey
ARG AwsSecretId
ARG AwsRegion
ENV AWS_ACCESS_KEY_ID=$AwsSecretId
ENV AWS_SECRET_ACCESS_KEY=$AwsSecretKey
ENV AWS_REGION=$AwsRegion
ENV GOOGLE_APPLICATION_CREDENTIALS="./localkey.json"
 
# Creates an app directory to hold your app’s source code
WORKDIR /app
 
# Copies everything from your root directory into /app
COPY . .
RUN apt-get update
RUN apt-get install curl -y curl jq
# --no-cache-dir
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install flask
EXPOSE 8080
EXPOSE 80
EXPOSE 443
ENTRYPOINT ["./startup.sh"]
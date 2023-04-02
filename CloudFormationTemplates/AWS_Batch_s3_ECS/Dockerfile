FROM python:3.8.13-slim-buster 


RUN apt-get update -y && apt-get install curl -y && \
    apt-get install unzip -y && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    mkdir -p src && \ 
    python --version && \
    aws --version
COPY ./sample.py src
WORKDIR /src
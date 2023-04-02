FROM python:3.8.13-slim-buster 
RUN mkdir -p src \ 
    && python --version \
    && python3 -m pip install awscliv2 \
    && aws --version
COPY ./sample.py src
WORKDIR /src
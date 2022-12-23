FROM ubuntu AS Checkout
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y git && \
    git clone https://github.com/awsdevops2022/aws.git


FROM python:3.8.13-slim-buster AS BuildStage

ARG AWS_DEFAULT_REGION
ARG AWS_SECRET_ACCESS_KEY 
ARG AWS_SESSION_TOKEN

ENV Region=$Region_name
 

RUN apt-get update -y && apt-get install curl -y && \
    apt-get install unzip -y && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install 
    # apt-get install python3-pip -y &&\
    # mkdir -p ./src 
RUN echo $AWS_ACCESS_KEY_ID 
RUN echo $AWS_SECRET_ACCESS_KEY 
RUN echo $AWS_SESSION_TOKEN 
RUN aws sts get-caller-identity 
RUN aws secretsmanager get-secret-value --secret-id test/HelloSecret --region ap-south-1

# WORKDIR /src
# COPY --from=Checkout aws/CloudFormationTemplates/AWSECS/example.py .
# RUN aws sts get-caller-identity && \
#     aws s3 cp . s3://bluewaterbucket
# CMD ["python3", "example.py"]

FROM ubuntu AS Checkout
RUN apt-get update -y && \
    apt-get install -y git && \
    git clone https://github.com/awsdevops2022/aws.git


FROM python:3.8.13-slim-buster AS BuildStage

ARG AWS_DEFAULT_REGION
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY 
ARG AWS_SESSION_TOKEN

ENV Region=$Region_name
 

RUN apt-get update -y && apt-get install curl -y && \
    apt-get install unzip -y && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    mkdir -p ./src && \
    echo $AWS_ACCESS_KEY_ID && \
    echo $AWS_SECRET_ACCESS_KEY && \
    echo $AWS_SESSION_TOKEN && \
    aws --version
    

WORKDIR /src
COPY --from=Checkout aws/CloudFormationTemplates/AWSECS/example.py .
RUN aws sts get-caller-identity && \
    aws s3 cp --recursive . s3://bluewaterbucket && \
    if [ $? -eq "0" ]; then echo "Upload to s3 successful on `date`"; else echo "Build failed"; fi
    
CMD ["python3", "example.py"]

FROM ubuntu as Checkout
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y git && \
    git clone https://github.com/awsdevops2022/aws.git


FROM python:3.8.13-slim-buster as BuildStage
ENV Region=$Region_name
RUN apt-get install -y wget && \
    apt-get install curl -y && \
    apt-get install unzip -y && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    aws --version && \
    apt-get -y install python3-pip \
    pip3 --version && \
    echo ${Region}


COPY --from=Checkout CloudFormationTemplates/AWSECS .
WORKDIR /AWSECS
CMD ["python", "example.py"]
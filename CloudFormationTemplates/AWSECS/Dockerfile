FROM amazonlinux:latest
RUN yum -y install aws-cli 
ARG AWS_DEFAULT_REGION
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY 
ARG AWS_SESSION_TOKEN 
RUN echo $AWS_ACCESS_KEY_ID 
RUN echo $AWS_SECRET_ACCESS_KEY 
RUN echo $AWS_SESSION_TOKEN 
RUN aws sts get-caller-identity 
RUN aws secretsmanager get-secret-value --secret-id test/HelloSecret --region ap-south-1
# To build a CI/CD process
    In this project we intend to demonstrate the CI/CD process when a pull request is made from GitHub (not push events) 
    containing Dockerfile to build a sample Python application in container images and run them using AWS Batch 
    as part of AWS Step Functions.

## AWS Resources 

 * `AWS SDK boto3`
 * `AWS CodeBuild`
 * `AWS CodePipeline`
 * `AWS Batch with ECS Fargate`
 * `AWS Step Functions`
 * `AWS S3`
 * `IAM Roles and Policies`
 * `AWS Lambda`

### :warning: Execution order of scripts
    The scripts must be executed/deployed in order as they have dependencies. 
    Make sure "AWS boto3" is setup. Please see below links for reference - 

 * `cb_eventbridge_stepfunctions_batch.yml`
 * `create_lambda.yml` 

 ### Useful links. 

 * `https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html`
 * `https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions.html#SFN.Client.start_execution`
 * `https://docs.aws.amazon.com/codebuild/latest/userguide/welcome.html`
 * `https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html`
 * `https://docs.aws.amazon.com/codepipeline/latest/userguide/welcome.html`
 * `https://docs.aws.amazon.com/batch/latest/userguide/what-is-batch.html`
 * `https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html`
 * `https://docs.aws.amazon.com/lambda/latest/dg/welcome.html`

Source - AWS. All rights reserved.
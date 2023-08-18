#!/usr/bin/env bash

# INSTALL NODE
# sudo yum install -y gcc-c++ make
# curl -sL https://rpm.nodesource.com/setup_16.x | sudo bash -
# sudo yum install -y nodejs


# INSTALL CDK
# npm install -g aws-cdk@2.92.0
# python3 -m venv .venv
# source .venv/bin/activate
# pip3 install -r requirements.txt


# DEPLOY STACK
ACCOUNT_ID=$(aws sts get-caller-identity --query Account | tr -d '"')
AWS_REGION=$(aws configure get region)
cdk bootstrap aws://${ACCOUNT_ID}/${AWS_REGION}
cdk deploy --parameters ProjectName=mlflow --require-approval never
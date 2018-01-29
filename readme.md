## Purpose
This tutorial demonstrates how to establish the architectural stack for training machine learning models on AWS, then deploy the machine learning model for real-time prediction. Primarily, it will cover using Sagemaker to train, evaluate, and deploy deep learning models developed in MXNet. This tutorial also includes the old content, which covers training and evaluating in EC2's Deep Learning AMI, then deploying in both Lambda and Batch.


## Prerequisites
- Basic knowledge of cloud computing basics
- Basic experience with Python
- Basic knowledge of Data Scient methodologies, specifically [CRISP-DM](https://en.wikipedia.org/wiki/Cross-industry_standard_process_for_data_mining)

## Recommended Sequence - [Sagemaker](sagemaker/)
### 1. Managed process using AWS Sagemaker
1. Start with [part0_instructions.md](sagemaker/part0_instructions.md), found in folder ['sagemaker'](sagemaker/)

### 2. Custom Process with EC2, Lambda, and Batch
1. CRISP-DM Parts 3-5, found in folder 'ec2-lambda-batch/crispdm345-training'
2. CRISP-DM 6 on AWS Lambda, found in folder 'ec2-lambda-batch/crispdm6-pred-lambda'
3. CRISP-DM 6 on AWS Batch, found in folder 'ec2-lambda-batch/crispdm6-pred-batch'


## Details
Author: Jake Chen (jakechen@amazon.com)

# Deploying a Pre-Trained MXNet to AWS Batch

## Create AMI
First, we need to create a Amazon Machine Image (AMI) that your Docker Containers will be running on top of. In our case, this machine image will need to have hooks to the GPU. We'll link to the [excellent official guide here, so no need to say more](http://docs.aws.amazon.com/batch/latest/userguide/batch-gpu-ami.html).

## Create Docker Image
SKIP
Use "mxnet/python:gpu"

## AWS Batch Setup
1. Create Compute Environment
	1. Select p2 family
	2. Use custom AMI created above
	3. Use all other defaults
2. Create Job Queue
	1. Set 1 as priority
	2. Select compute env from above
3. Create Job Definition
	1. 
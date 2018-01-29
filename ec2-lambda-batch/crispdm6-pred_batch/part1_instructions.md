# Deploying a Pre-Trained MXNet to AWS Batch
Combination of blogs: 
- ["Creating a Simple “Fetch & Run” AWS Batch Job"](https://aws.amazon.com/blogs/compute/creating-a-simple-fetch-and-run-aws-batch-job/)
- ["Deep Learning on AWS Batch"](https://aws.amazon.com/blogs/compute/deep-learning-on-aws-batch/)


## Create GPU AMI and Docker Images
### Create GPU AMI
First, we need to create a Amazon Machine Image (AMI) that your Docker Containers will be running on top of. In our case, this machine image will need to have hooks to the GPU. We'll link to the [excellent official guide here, so no need to say more](http://docs.aws.amazon.com/batch/latest/userguide/batch-gpu-ami.html). Don't terminate this instance yet!

### Create and Register Docker Image
Now in the same EC2 instance above, we can also create the Docker Image that will be registered to ECS Repository.

1. Create Dockerfile
```
FROM amazonlinux

RUN yum -y upgrade
RUN yum install -y python27-pip
RUN yum install -y libgomp
RUN pip install mxnet
RUN pip install boto3

COPY src/part2_pred_script.py /tmp/part2_pred_script.py

ENTRYPOINT ["python", "/tmp/part2_pred_script.py"]
```
2. Build Docker Image
```
docker build -t mnist_predictor .
```
3. Register Docker Image to ECR
Follow these steps in AWS Console:
	1. [Open ECS console](https://console.aws.amazon.com/ecs)
	2. Click Repositories on the left, click "Create Repository"
	3. Fill out form fields
	4. Follow directions out the screen
	5. Keep a record of the Repository URI


## AWS Batch Setup
1. Create Compute Environment
	1. Select p2 family
	2. Use custom AMI created above
	3. Use all other defaults
2. Create Job Queue
	1. Set 1 as priority
	2. Select compute env from above
3. Create Job Definition
	1. In "Container Image", input the ECS Repository URI from above
	2. Leave everything else as default
4. Submit a job
	1. Use the Job Definition from above
	2. Use the Job Queue from above
	3. Submit!
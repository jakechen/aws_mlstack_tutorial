# Deploying a Pre-Trained MXNet to AWS Lambda
The following steps are based on the official Lambda Functions documentation, specifically [Create Deployment Package Using a Python Environment Created with Virtualenv](http://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html#deployment-pkg-for-virtualenv)

## Gotchas
- unzipped needs to be within 240MB
- best to cd into the directory, then zip -r -9 ../lambda.zip *
- remember your .py script name and the function inside
- only /tmp/ directory is writeable, so s3.download_file() your objects there

## Author and Test Prediction Script in EC2

### Spin up EC2 instance
1. On [this page](http://docs.aws.amazon.com/lambda/latest/dg/current-supported-versions.html), find the AMI that AWS Lambda is based on.
2. Launch an EC2 instance using this AMI. One of the T2 instances will suffice.
3. SSH into this instance as normal

### Install required libraries script
1. Create the Python environment
```
virtualenv ~/mxnet
```
2. Activate the environment
```
source ~/mxnet/bin/activate
```
3. Install MXNet into this environment
```
pip install mxnet boto3
```

### Author and test prediction script
1. Create your project directory and project code
```
mkdir ~/lambda
touch ~/lambda/lambda_function.py
```
2. Write your Lambda function
	1. In this tutorial, simply copy the prediction script part2_pred_script.py
3. Run your function and confirm it works before moving on
```
python ~/lambda/lambda_function.py
```

## Create Deployment Packages
1. Move packages into the same directory as your script, such as:
```
cp -r ~/mxnet/lib/python2.7/site-packages/* ~/lambda/
cp -r ~/mxnet/lib64/python2.7/site-packages/* ~/lambda/
```
2. Zip up all files into the Deployment Package
```
cd ~/lambda
zip -r -9 --exclude="*.pyc" ../lambda.zip ./*
```
3. Upload Deployment Package onto S3
```
aws s3 cp ../lambda.zip s3://jakechenawstemp/
```

## Create Lambda Function
[Official documentation here](http://docs.aws.amazon.com/lambda/latest/dg/with-userapp-walkthrough-custom-events-upload.html).
1. In AWS Console
	1. If you haven't already, [create an IAM Role for Lambda](http://docs.aws.amazon.com/lambda/latest/dg/with-userapp-walkthrough-custom-events-create-iam-role.html).
	2. Create a new Lambda Function and point to your zip in S3
2. Or in AWS CLI
	1. If you haven't already, [create an IAM Role for Lambda](http://docs.aws.amazon.com/lambda/latest/dg/with-userapp-walkthrough-custom-events-create-iam-role.html)
	2. Run this CLI code
	```
	aws lambda create-function \
	--region us-east-1 \
	--function-name mnist_predictor \
	--code S3Bucket=jakechenawstemp, S3Key=lambda.zip \ # change this to where you uploaded your zipped Deployment Package
	--role admin_lambda \ # change this to the role you made
	--handler lambda_function.lambda_handler \
	--runtime python2.7 \
	--profile adminuser 
	```
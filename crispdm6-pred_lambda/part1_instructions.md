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
1. Create the Python environment using
```
virtualenv ~/mxnet
```
2. Activate the environment using `source ~/mxnet/bin/activate`
3. Install MXNet into this environment using `pip install mxnet boto3`

### Author and test prediction script
1. Create your project directory, such as:
	1. `mkdir ~/lambda`
	2. `touch ~/lambda/lambda_function.py`
2. Write your Lambda function
	1. In this tutorial, simply copy the prediction script part2_pred_script.py
3. Run your function and confirm it works before moving on using `python ~/lambda/lambda_function.py`

## Create Deployment Packages
1. Move packages into the same directory as your script, such as:
	1. `cp -r ~/mxnet/lib/python2.7/site-packages/* ~/lambda/`
	2. `cp -r ~/mxnet/lib64/python2.7/site-packages/* ~/lambda/`
2. Zip up all files into the deployment package
	1. `cd ~/lambda`
	2. `zip -r -9 --exclude="*.pyc" ../lambda.zip ./*`
3. Upload deployment package onto S3
	1. `aws s3 cp ../lambda.zip s3://jakechenawstemp/`

## Create Lambda Function
1. In AWS Console, create a new Lambda Function and point to your zip in S3
	1. 
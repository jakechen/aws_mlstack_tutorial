# -*- coding: utf-8 -*-
"""
Generic baseline model training script with the following steps:
1. Read data from S3
2. Simple model cleansing
3. Split test/train
4. Train model
5. Evaluate model
6. Save model into S3
"""

import boto3
import pandas as pd
import sklearn

# Read data from S3
s3 = boto3.resource('s3')

# Readme.md
Using Amazon Sagemaker to ease training, evaluating, and deployment of MXNet models.

## 1. Model Research
Define and train model as usual in Jupter Notebook to ensure it works.

Please open [part1\_model\_research.ipynb](./part1_model_research.ipynb) to begin.


## 2. Model Development for SageMaker
Refactor the training code from [part1\_model\_research.ipynb](./part1_model_research.ipynb) into this [Sagemaker .py template](http://docs.aws.amazon.com/sagemaker/latest/dg/mxnet-training-inference-code-template.html).

Since the code is already working, the primary change we will be making is to use MXNet's distributed training capabilities. For details, refer to [this guide](https://mxnet.incubator.apache.org/how_to/multi_devices.html).

Please see [part2\_sm\_mnist.py](./part2_sm_mnist.py) for a completed version.


## 3. Model Training and Evaluation using SageMaker


## 4. Model Deployment using SageMaker


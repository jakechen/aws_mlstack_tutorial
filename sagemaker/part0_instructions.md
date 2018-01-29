# Readme.md
In this tutorial, we will be demonstrating how to use Amazon Sagemaker to ease training, evaluating, and deployment of MXNet models.

## 0. Introduction
Amazon Sagemaker is a managed service designed to streamline the process of training, evaluating, and deploying machine learning models. There are a few different pieces, but the Data Scientists generally interface with the Jupyter Notebook and the Sagemaker API.

To begin, Sagemaker can launch a Jupyter Notebook instance that reproduces the common Python scientific computing stack within minutes, allowing Data Scientists to quickly connect to their data, then import and utilize familiar libraries such numpy, pandas, sklearn, mxnet, and tensorflow. On top of this, it also allows the user to use the Sagemaker API.

The Sagemaker API allows a Data Scientist to:

1. Train a model across a fleet of CPU or GPU resources. This model is generally:
    a. One of a dozen optmized ML algos chosen to address common ML tasks e.g. regression, classification, recommendation, etc
    b. A custom Neural Network built using MXNet (or Gluon, etc)
    c. A custom Neural Network buildt using Tensorflow (or Keras, etc)s
2. Deploy the trained model above onto 1+ CPU or GPU instance(s) and receive the associated API endpoint.

In the following steps, we will demonstrate how to train an MNIST classifier using MXNet on Sagemaker.


## 1. Model Research
First, we will define the MXNet model as usual in Jupter Notebook. We will then train it locally to ensure it works.

Please open [part1\_model\_research.ipynb](./part1_model_research.ipynb) to begin.


## 2. Model Development for SageMaker
While the model we defined above can be trained locally, Sagemaker can provision a fleet of compute resources and then train the model across that fleet. For very simple models, this benefit will not be immediately apparent, but this scalability is important for complex models.

To take advantage of this feature, we must Refactor the training code from [part1\_model\_research.ipynb](./part1_model_research.ipynb) into this [Sagemaker .py template](http://docs.aws.amazon.com/sagemaker/latest/dg/mxnet-training-inference-code-template.html). Be aware that some of the functions defined in this template will not be needed. We remove these functions because Sagemaker will default to the built-in functions. For example, Sagemaker's MXNet wrapper will automatically save the model, generally negating the need for a custom save() function. For more information on the default actions take, refer to [this documentation](https://github.com/aws/sagemaker-python-sdk).

In our case, since the code is already working, the primary change we will be making is to use MXNet's distributed training capabilities. For details, refer to [this guide](https://mxnet.incubator.apache.org/how_to/multi_devices.html).

Please see [part2\_sm\_mnist.py](./part2_sm_mnist.py) for a completed version.

## 3. Model Training, Evaluation, and Deployment using SageMaker
Once we have our MXNet training script from Step 2, we now use the Sagemaker API to launch of cluster of instances and push the training across this cluster. This should only take a few lines of code. After the training is completed, we can then use Sagemaker to deploy the trained model across 1+ instances. Again, this should also only take a few lines of code. Once the deployment is complete, Sagemaker returns an API endpoint that all new records can be fed into for a real-time prediction.

Please see [part3\_model\_training.ipynb](./part3_model_training.ipynb) for a step-by-step demonstration of these capabilities.

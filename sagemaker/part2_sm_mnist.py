#
#
# Templates for required and optional functions for this file can be found here:
# http://docs.aws.amazon.com/sagemaker/latest/dg/mxnet-training-inference-code-template.html
#
# More information can be found here:
# https://github.com/aws/sagemaker-python-sdk#sagemaker-python-sdk-overview
#


# https://github.com/aws/sagemaker-python-sdk#preparing-the-mxnet-training-script
import logging
import mxnet as mx
import numpy as np
from glob import glob

# ---------------------------------------------------------------------------- #
# Training functions                                                           #
# ---------------------------------------------------------------------------- #
def train(channel_input_dirs, **kwargs):

    """
    [Required]

    Runs Apache MXNet training. Amazon SageMaker calls this function with information
    about the training environment. When called, if this function returns an
    object, that object is passed to a save function.  The save function
    can be used to serialize the model to the Amazon SageMaker training job model
    directory.

    The **kwargs parameter can be used to absorb any Amazon SageMaker parameters that
    your training job doesn't need to use. For example, if your training job
    doesn't need to know anything about the training environment, your function
    signature can be as simple as train(**kwargs).

    Amazon SageMaker invokes your train function with the following python kwargs:

    Args:
        - hyperparameters: The Amazon SageMaker Hyperparameters dictionary. A dict
            of string to string.
        - input_data_config: The Amazon SageMaker input channel configuration for
            this job.
        - channel_input_dirs: A dict of string-to-string maps from the
            Amazon SageMaker algorithm input channel name to the directory containing
            files for that input channel. Note, if the Amazon SageMaker training job
            is run in PIPE mode, this dictionary will be empty.
        - output_data_dir:
            The Amazon SageMaker output data directory. After the function returns, data written to this
            directory is made available in the Amazon SageMaker training job
            output location.
        - model_dir: The Amazon SageMaker model directory. After the function returns, data written to this
            directory is made available to the Amazon SageMaker training job
            model location.
        - num_gpus: The number of GPU devices available on the host this script
            is being executed on.
        - num_cpus: The number of CPU devices available on the host this script
            is being executed on.
        - hosts: A list of hostnames in the Amazon SageMaker training job cluster.
        - current_host: This host's name. It will exist in the hosts list.
        - kwargs: Other keyword args.

    Returns:
        - (object): Optional. An Apache MXNet model to be passed to the model
            save function. If you do not return anything (or return None),
            the save function is not called.
    """

    #
    # Sagemaker API automatically downloads the files when we call fit() on the Estimator
    # We can find where these files are in the channel_input_dirs dict, which is an argument into this function.
    # This isn't always needed (e.g. hard coded files), but is cleaner b/c fit() requires an 'input' argument
    #
    
    # load downloaded files into s3
    logging.info('training images directory detected as: {}'.format(channel_input_dirs['images']))
    logging.info('training labels directory detected as: {}'.format(channel_input_dirs['labels']))
    
    # load downloaded files into numpy arrays
    f_name = channel_input_dirs['images']+'/images.csv'
    X_arrays = np.loadtxt(f_name, delimiter=',')

    f_name = channel_input_dirs['labels']+'/labels.csv'
    y_arrays = np.loadtxt(f_name, delimiter=',')
    
    # reshape into requisite shape for NN
    X_train = X_arrays.reshape(-1, 1, 28, 28)
    y_train = y_arrays.reshape(-1)
    logging.info('X_train.shape: {}'.format(X_train.shape))
    logging.info('y_train.shape: {}'.format(y_train.shape))
    
    # wrap mxnet iterator around records
    batch_size = 100
    train_iter = mx.io.NDArrayIter(X_train, y_train, batch_size, shuffle=True)
    
    """
    Begin copy/paste from tutorial part 1
    """
    # define network
    data = mx.sym.var('data')
    # first conv layer
    conv1 = mx.sym.Convolution(data=data, kernel=(5,5), num_filter=20)
    tanh1 = mx.sym.Activation(data=conv1, act_type="tanh")
    pool1 = mx.sym.Pooling(data=tanh1, pool_type="max", kernel=(2,2), stride=(2,2))
    # second conv layer
    conv2 = mx.sym.Convolution(data=pool1, kernel=(5,5), num_filter=50)
    tanh2 = mx.sym.Activation(data=conv2, act_type="tanh")
    pool2 = mx.sym.Pooling(data=tanh2, pool_type="max", kernel=(2,2), stride=(2,2))
    # first fullc layer
    flatten = mx.sym.flatten(data=pool2)
    fc1 = mx.symbol.FullyConnected(data=flatten, num_hidden=500)
    tanh3 = mx.sym.Activation(data=fc1, act_type="tanh")
    # second fullc
    fc2 = mx.sym.FullyConnected(data=tanh3, num_hidden=10)
    # softmax loss
    lenet = mx.sym.SoftmaxOutput(data=fc2, name='softmax')

    """
    End copy/paste from tutorial part 1
    """

    # create a trainable module
    context=mx.gpu() # change to mx.gpu() if using ml.p2.xlarge

    # Toggle this between 'local', 'device', 'dist-sync', or 'dist-device-sync' 
    # depending on if you're using ml.c-family or ml.p-family for training.
    #
    # For more info: https://mxnet.incubator.apache.org/how_to/multi_devices.html
    kvstore='device'
    
    lenet_model = mx.mod.Module(symbol=lenet, context=context)
    lenet_model.fit(train_iter,
                    optimizer='sgd',
                    optimizer_params={'learning_rate':0.1},
                    num_epoch=5,
                    kvstore=kvstore # added kvstore argument
                   )
    
    return lenet_model
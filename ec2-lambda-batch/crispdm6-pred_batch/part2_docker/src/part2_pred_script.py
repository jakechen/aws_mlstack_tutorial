batch_size = 5

import mxnet as mx
import numpy as np
import boto3


s3 = boto3.client('s3')

# Download saved model
s3.download_file(
    'jakechenawstemp',
    'mnist_symbol.mxnet',
    '/tmp/mnist_symbol.mxnet'
)
s3.download_file(
    'jakechenawstemp',
    'mnist_module.mxnet',
    '/tmp/mnist_module.mxnet'
)

# Download latest 5 records
s3.download_file(
    'jakechenawstemp',
    'x_test.csv',
    '/tmp/x_test.csv'
)
s3.download_file(
    'jakechenawstemp',
    'y_test.csv',
    '/tmp/y_test.csv'
)

# Load and run predictions using saved model
def lambda_handler(event, context):
    X_test = np.fromfile('/tmp/x_test.csv', sep=',').reshape((-1,1,28,28))
    y_test = np.fromfile('/tmp/y_test.csv', sep=',')

    test_iter = mx.io.NDArrayIter(
        data = X_test,
        label = y_test,
        batch_size = batch_size)

    lenet2 = mx.symbol.load('/tmp/mnist_symbol.mxnet')
    lenet_model2 = mx.mod.Module(lenet2, context=mx.cpu())
    lenet_model2.bind(test_iter.provide_data, test_iter.provide_label, for_training=False)
    lenet_model2.load_params('/tmp/mnist_module.mxnet')

    y_proba = lenet_model2.predict(test_iter)
    y_pred = mx.ndarray.argmax(y_proba, axis=1)
    return y_pred.asnumpy().tolist()

# For local testing
if __name__ == '__main__':
    y_pred = lambda_handler('','')
    print(y_pred)

batch_size = 5

import mxnet as mx
import boto3


s3 = boto3.client('s3')

# Download saved model
s3.download_file(
    'jakechenawstemp',
    'mnist_symbol.mxnet',
    './mnist_symbol.mxnet'
)
s3.download_file(
    'jakechenawstemp',
    'mnist_module.mxnet',
    './mnist_module.mxnet'
)

# Download latest 5 records
s3.download_file(
    'jakechenawstemp',
    'x_test.csv',
    './x_test.csv'
)
s3.download_file(
    'jakechenawstemp',
    'y_test.csv',
    './y_test.csv'
)

# Load and run predictions using saved model
def lambda_handler(event, context):
    test_iter = mx.io.CSVIter(
        data_csv = './x_test.csv',
        data_shape = (1, 28, 28),
        label_csv= './y_test.csv',
        label_shape = (5,),
        batch_size = batch_size)

    lenet2 = mx.symbol.load('./mnist_symbol.mxnet')
    lenet_model2 = mx.mod.Module(lenet2, context=mx.cpu())
    lenet_model2.bind(test_iter.provide_data, test_iter.provide_label, for_training=False)
    lenet_model2.load_params('./mnist_module.mxnet')

    acc = mx.metric.Accuracy()
    lenet_model2.score(test_iter, acc)

    return acc

# For local testing
if __name__ == '__main__':
    acc = lambda_handler('','')
    print(acc)

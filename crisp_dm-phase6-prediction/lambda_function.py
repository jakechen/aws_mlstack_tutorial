batch_size = 10

import mxnet as mx
import boto3

s3 = boto3.client('s3')
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

mnist = mx.test_utils.get_mnist()
test_iter = mx.io.NDArrayIter(mnist['test_data'], mnist['test_label'], batch_size)

type(mnist['test_data'][0])

lenet2 = mx.symbol.load('./mnist_symbol.mxnet')
lenet_model2 = mx.mod.Module(lenet2, context=mx.gpu())
lenet_model2.bind(test_iter.provide_data, test_iter.provide_label, for_training=False)
lenet_model2.load_params('./mnist_module.mxnet')

acc = mx.metric.Accuracy()
lenet_model2.score(test_iter, acc)
print(acc)
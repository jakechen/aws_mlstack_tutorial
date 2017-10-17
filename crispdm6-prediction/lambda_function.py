batch_size = 1

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

def lambda_handler(event, context)
	X = mx.io.NDArrayIter(mnist['test_data'], mnist['test_label'], batch_size)

	lenet2 = mx.symbol.load('./mnist_symbol.mxnet')
	lenet_model2 = mx.mod.Module(lenet2, context=mx.gpu())
	lenet_model2.bind(X.provide_data, X.provide_label, for_training=False)
	lenet_model2.load_params('./mnist_module.mxnet')
	
	acc = mx.metric.Accuracy()
	lenet_model2.score(X, acc)
	print(acc)
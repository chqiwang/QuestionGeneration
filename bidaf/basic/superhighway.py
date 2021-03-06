import tensorflow as tf
from tensorflow.python.ops.rnn_cell import RNNCell

from my.tensorflow.nn import linear


class SHCell(RNNCell):
    """
    Super-Highway Cell
    """
    def __init__(self, input_size, logit_func='tri_linear', scalar=True, bias=3.0):
        self._state_size = input_size
        self._output_size = input_size
        self._logit_func = logit_func
        self._scalar = scalar
        self._bias = bias

    @property
    def state_size(self):
        return self._state_size

    @property
    def output_size(self):
        return self._output_size

    def __call__(self, inputs, state, scope=None):
        with tf.variable_scope(scope or "SHCell"):
            a_size = 1 if self._scalar else self._state_size
            h, u = tf.split(1, 2, inputs)
            if self._logit_func == 'mul_linear':
                args = [h * u]
                a = tf.nn.sigmoid(linear(args, a_size, True, bias_start=self._bias, scope='a'))
                r = tf.nn.sigmoid(linear(args, a_size, True, bias_start=self._bias, scope='r'))
            elif self._logit_func == 'linear':
                args = [h, u]
                a = tf.nn.sigmoid(linear(args, a_size, True, bias_start=self._bias, scope='a'))
                r = tf.nn.sigmoid(linear(args, a_size, True, bias_start=self._bias, scope='r'))
            elif self._logit_func == 'tri_linear':
                args = [h, u, h * u]
                a = tf.nn.sigmoid(linear(args, a_size, True, bias_start=self._bias, scope='a'))
                r = tf.nn.sigmoid(linear(args, a_size, True, bias_start=self._bias, scope='r'))
            elif self._logit_func == 'double':
                args = [h, u]
                a = tf.nn.sigmoid(linear(tf.tanh(linear(args, a_size, True)), self._state_size, True, bias_start=self._bias))
                r = tf.nn.sigmoid(linear(tf.tanh(linear(args, a_size, True)), self._state_size, True, bias_start=self._bias))

            else:
                raise Exception()
            new_state = a * state + r * (1 - a) * h
            outputs = state
            return outputs, new_state


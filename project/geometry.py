import numpy as np
import tensorflow as tf


def cos_squash(_input, name=None):
    """
    Squashes real-values to the range (-pi, pi].
    :param _input: real-valued tensor-like input
    :param name: optional name for tensor
    :return: values squashed to the range(-pi, pi)
    """
    with tf.name_scope(name, 'cos_squash', [_input]) as scope:
        input_tensor = tf.convert_to_tensor(_input, name='input')

        return tf.multiply(np.pi, tf.cos(input_tensor + np.pi / 2), name=scope)

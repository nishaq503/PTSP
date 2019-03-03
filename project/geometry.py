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


def mean_angle(radii, angles, name=None):
    """
    Computes the geometric mean of angles weighted by radii.
    :param radii: radii in tensor-like form. [batch_sz, num_angles]
    :param angles: angles in tensor-like form. [num_angles, num_dihedrals]
    :param name: optional name for scope.
    :return: weighted geometric mean of angles. [batch_sz, num_dihedrals]
    """
    with tf.name_scope(name, 'mean_angle', [radii, angles]) as scope:
        radii_tensor = tf.convert_to_tensor(radii, name='radii')
        angles_tensor = tf.convert_to_tensor(angles, name='angles')

        y_s = tf.matmul(radii_tensor, tf.sin(angles_tensor))
        x_s = tf.matmul(angles_tensor, tf.cos(angles_tensor))

        return tf.atan2(y_s, x_s, name=scope)


def reduce_l2_norm(_input,
                   weights=None,
                   reduction_indexes=None,
                   keep_dims=None,
                   epsilon=1e-12,
                   name=None):
    """
    computes the l2_norm of the input along the dimensions in reduction_indexes.
    :param _input: tensor-like input.
    :param weights: tensor-like weights.
    :param reduction_indexes: which dimensions to calculate l2_norm for.
    :param keep_dims: which dimensions to keep.
    :param epsilon: lowest allowed precision
    :param name: optional name for scope
    :return: tensor of l2_norm along given dimensions
    """
    with tf.name_scope(name, 'reduce_l2_norm', [_input, weights]) as scope:
        input_tensor = tf.convert_to_tensor(_input, name='_input')

        input_tensor_squared = tf.square(input_tensor)
        if weights:
            weights_tensor = tf.convert_to_tensor(weights, name='weights')
            input_tensor_squared *= weights_tensor

        return tf.sqrt(tf.maximum(tf.reduce_sum(input_tensor_squared,
                                                axis=reduction_indexes,
                                                keep_dims=keep_dims),
                                  epsilon),
                       name=scope)


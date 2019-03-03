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


def pairwise_distances(_input, name=None):
    """
    computes the pairwise distances between all vectors in the input.
    vectors are to be in 3-D
    :param _input: tensor-like input [num_steps, batch_sz, num_dimensions]
    :param name: optional name
    :return: pairwise distances between vectors in _input [num_steps, num_steps, batch_sz]
    """
    with tf.name_scope(name, 'pairwise_distances', [_input]) as scope:
        input_tensor = tf.convert_to_tensor(_input, name='input')
        return reduce_l2_norm(input_tensor - tf.expand_dims(input_tensor, 1),
                              reduction_indexes=[3],
                              name=scope)


def drmsd(x, y, weights, name=None):
    """
    computes the dRMSD of two tensors of vectors.
    :param x: tensor-like input containing 3-D vectors [num_steps, batch_sz, num_dimensions]
    :param y: tensor-like input containing 3-D vectors [num_steps, batch_sz, num_dimensions]
    :param weights: tensor-like weights [num_steps, num_steps, batch_sz]
    :param name: optional name
    :return: dRMSD between x and y. [batch_sz]
    """
    with tf.name_scope(name, 'dRMSD', [x, y, weights]) as scope:
        x_tensor = tf.convert_to_tensor(x, name='x')
        y_tensor = tf.convert_to_tensor(y, name='y')
        weights_tensor = tf.convert_to_tensor(weights, name='weights')
        return reduce_l2_norm(pairwise_distances(x_tensor) - pairwise_distances(y_tensor),
                              reduction_indexes=[0, 1],
                              weights=weights_tensor,
                              name=scope)

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


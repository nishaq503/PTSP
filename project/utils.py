import re

import tensorflow as tf

# Constants
NUM_DIMENSIONS = 3


def _features(d):
    return tf.train.Features(feature=d)


def _feature_list(l):
    return tf.train.FeatureList(feature=l)


def _feature_lists(d):
    return tf.train.FeatureLists(feature_list=d)


def _bytes_feature(v):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=v))


def _int64_feature(v):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=v))


def _float_feature(v):
    return tf.train.Feature(float_list=tf.train.FloatList(value=v))


def string_to_num_list(string, dict_):
    """
    Convert a string of letters into a list of ints using the dictionary provided
    :param string: string of letters
    :param dict_: dictionary to use
    :return: list of ints
    """
    pattern = re.compile('[' + ''.join(dict_.keys()) + ']')
    num_string = pattern.sub(lambda m: dict_[m.group(0)] + ' ', string)
    return [int(i) for i in num_string.split()]


def file_to_dict(infile, num_entries):
    """

    :param infile: file to read
    :param num_entries: pssm entries
    :return: dictionary that was created
    """
    # Dictionaries for dealing with input data
    _aa_dict = {'A': '0', 'C': '1', 'D': '2', 'E': '3', 'F': '4', 'G': '5', 'H': '6', 'I': '7', 'K': '8', 'L': '9',
                'M': '10', 'N': '11', 'P': '12', 'Q': '13', 'R': '14', 'S': '15', 'T': '16', 'V': '17', 'W': '18',
                'Y': '19'}
    _dssp_dict = {'L': '0', 'H': '1', 'B': '2', 'E': '3', 'G': '4', 'I': '5', 'T': '6', 'S': '7'}
    _mask_dict = {'-': '0', '+': '1'}

    dict_ = {}

    while True:
        line = infile.readline()

        if line == '[ID]' + '\n':
            id_ = infile.readline()[: -1]
            dict_.update({'id': id_})

        elif line == '[PRIMARY]' + '\n':
            primary = string_to_num_list(infile.readline()[:-1], _aa_dict)
            dict_.update({'primary': primary})

        elif line == '[EVOLUTIONARY]' + '\n':
            evolutionary = []
            for residue in range(num_entries):
                evolutionary.append([float(step) for step in infile.readline().split()])
            dict_.update({'evolutionary': evolutionary})

        elif line == '[SECONDARY]' + '\n':
            secondary = string_to_num_list(infile.readline()[:-1], _dssp_dict)
            dict_.update({'secondary': secondary})

        elif line == '[TERTIARY]' + '\n':
            tertiary = []
            for axis in range(NUM_DIMENSIONS):
                tertiary.append([float(coord) for coord in infile.readline().split()])
            dict_.update({'tertiary': tertiary})

        elif line == '[MASK]' + '\n':
            mask = string_to_num_list(infile.readline()[:-1], _mask_dict)
            dict_.update({'mask': mask})

        elif line == '\n':
            return dict_

        elif line == '':
            return None


def dict_to_tfrecord(dict_):
    """
    convert a given dictionary into a tfrecord.
    :param dict_: dictionary to convert
    :return: TFRecord
    """

    id_ = _bytes_feature([dict_['id']])

    feature_lists_dict = {}
    feature_lists_dict.update(
        {'primary': _feature_list([_int64_feature([aa]) for aa in dict_['primary']])}
    )

    if 'evolutionary' in dict_:
        feature_lists_dict.update(
            {'evolutionary': _feature_list([_float_feature(list(step)) for step in zip(*dict_['evolutionary'])])}
        )

    if 'secondary' in dict_:
        feature_lists_dict.update({'secondary': _feature_list([_int64_feature([dssp]) for dssp in dict_['secondary']])}
                                  )

    if 'tertiary' in dict_:
        feature_lists_dict.update(
            {'tertiary': _feature_list([_float_feature(list(coord)) for coord in zip(*dict_['tertiary'])])}
        )

    if 'mask' in dict_:
        feature_lists_dict.update(
            {'mask': _feature_list([_float_feature([step]) for step in dict_['mask']])}
        )

    tfrecord = tf.train.SequenceExample(
        context=_features({'id': id_}),
        feature_lists=_feature_lists(feature_lists_dict)
    )

    return tfrecord

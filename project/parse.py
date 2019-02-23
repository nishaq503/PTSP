import re
import sys

import tensorflow as tf

from project.utilities import Switch


# Constants
NUM_DIMENSIONS = 3

# helpers for dealing with TF Example etc and make code more verbose
# Accessory functions for dealing with TF Example and SequenceExample
_example = tf.train.Example
_sequence_example = tf.train.SequenceExample
_feature = tf.train.Feature
_features = lambda d: tf.train.Features(feature=d)
_feature_list = lambda l: tf.train.FeatureList(feature=l)
_feature_lists = lambda d: tf.train.FeatureLists(feature_list=d)
_bytes_feature = lambda v: _feature(bytes_list=tf.train.BytesList(value=v))
_int64_feature = lambda v: _feature(int64_list=tf.train.Int64List(value=v))
_float_feature = lambda v: _feature(float_list=tf.train.FloatList(value=v))

# Dictionaries for dealing with input data
_aa_dict = {'A': '0', 'C': '1', 'D': '2', 'E': '3', 'F': '4', 'G': '5', 'H': '6', 'I': '7', 'K': '8', 'L': '9', 'M': '10', 'N': '11', 'P': '12', 'Q': '13', 'R': '14', 'S': '15', 'T': '16', 'V': '17', 'W': '18', 'Y': '19'}
_dssp_dict = {'L': '0', 'H': '1', 'B': '2', 'E': '3', 'G': '4', 'I': '5', 'T': '6', 'S': '7'}
_mask_dict = {'-': '0', '+': '1'}


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


def record_to_dict(infile, num_entries):
    """

    :param infile:
    :param num_entries:
    :return:
    """

    dict_ = {}

    while True:
        line = infile.readline()
        for case in Switch(line):
            if case('[ID]' + '\n'):
                id_ = infile.readline()[: -1]
                dict_.update({'id': id_})
            elif case('[PRIMARY]' + '\n'):
                primary = string_to_num_list(infile.readline()[:-1], _aa_dict)
                dict_.update({'primary': primary})
            elif case('[EVOLUTIONARY]' + '\n'):
                evolutionary = []
                for residue in range(num_entries):
                    evolutionary.append([float(step) for step in infile.readline().split()])
                dict_.update({'evolutionary': evolutionary})
            elif case('[SECONDARY]' + '\n'):
                secondary = string_to_num_list(infile.readline()[:-1], _dssp_dict)
                dict_.update({'secondary': secondary})
            elif case('[TERTIARY]' + '\n'):
                tertiary = []
                for axis in range(NUM_DIMENSIONS):
                    tertiary.append([float(coord) for coord in infile.readline().split()])
                dict_.update({'tertiary': tertiary})
            elif case('[MASK]' + '\n'):
                mask = string_to_num_list(infile.readline()[:-1], _mask_dict)
                dict_.update({'mask': mask})
            elif case('\n'):
                return dict_
            elif case(''):
                return None


def dict_to_tfrecord(dict_):
    """
    convert a given dictionary into a tfrecord.
    :param dict_: dictionary to convert
    :return: TFRecord
    """

    id_ = _bytes_feature([dict_['id']])

    feature_lists_dict = {}
    feature_lists_dict.update({'primary': _feature_list([_int64_feature([aa]) for aa in dict_['primary']])})

    if dict_.has_key('evolutionary'):
        feature_lists_dict.update({'evolutionary': _feature_list([_float_feature(list(step)) for step in zip(*dict_['evolutionary'])])})

    if dict_.has_key('secondary'):
        feature_lists_dict.update({'secondary': _feature_list([_int64_feature([dssp]) for dssp in dict_['secondary']])})

    if dict_.has_key('tertiary'):
        feature_lists_dict.update({'tertiary': _feature_list([_float_feature(list(coord)) for coord in zip(*dict_['tertiary'])])})

    if dict_.has_key('mask'):
        feature_lists_dict.update({'mask': _feature_list([_float_feature([step]) for step in dict_['mask']])})

    record = _sequence_example(context=_features({'id': id_}), feature_lists=_feature_lists(feature_lists_dict))

    return record


if __name__ == '__main__':
    """
    main.
    Accepts 3 command line arguments.
    :param input_path: path of file to read
    :param output_path: path of file to write
    :param num_entries: number of entries. defaults to 20.
    """
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    num_entries = int(sys.argv[3]) if len(sys.argv) == 4 else 20

    with open(input_path, 'r') as infile, tf.python_io.TFRecordWriter(output_path) as outfile:

        while True:
            dict_ = record_to_dict(infile, num_entries)
            if dict_ is not None:
                serialized_tf_record = dict_to_tfrecord(dict_).SerializeToString()
                outfile.write(serialized_tf_record)
            else:
                break

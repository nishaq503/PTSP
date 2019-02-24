import sys

import tensorflow as tf

from project.utilities import file_to_dict, dict_to_tfrecord


def text_to_tfrecord(input_path, output_path, num_entries):
    """
    :param input_path: path of file to read.
    :param output_path: path of file to write.
    :param num_entries: number of entries.
    """
    with open(input_path, 'r') as infile, tf.python_io.TFRecordWriter(output_path) as outfile:

        while True:
            dict_ = file_to_dict(infile, num_entries)

            if dict_:
                serialized_tf_record = dict_to_tfrecord(dict_).SerializeToString()
                outfile.write(serialized_tf_record)

            else:
                break
    return


if __name__ == '__main__':
    file_in, file_out = sys.argv[1], sys.argv[2]
    entries = int(sys.argv[3]) if len(sys.argv) == 4 else 20
    text_to_tfrecord(file_in, file_out, entries)

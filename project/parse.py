
def make_training_example(lines):
    """
    Takes lines read from file and created a training example.

    :param lines: raw lines read from text file

    :return: training example as a dictionary
    """
    example = {}
    
    example['id'] = lines[1].rstrip()
    example['primary'] = lines[3].rstrip()
    
    pssm = []
    for i in range(5, 26):
        pssm.append([float(x) for x in lines[i].split()])
    example['pssm'] = pssm
    
    tertiary = []
    for i in range(27, 30):
        tertiary.append([float(x) for x in lines[i].split()])
    example['tertiary'] = tertiary
    
    example['mask'] = lines[31].rstrip()
    
    return example

def parse_training_data(
    input_file_path="data/text_based/training/training_100",
    output_file_path="data/parsed/training/training_100"
    ):
    """
    This function opens a text-based file with training data, reads the examples, and writes them to binary tfRecords files for ease of use when training begins.

    :param input_file_path: defaults to location on Najib's computer
    :param output_file_path: defaults to location on Najib's computer
    """

    with open(input_file_path, 'r') as raw_data:
        lines, examples = [], []
        for line in raw_data:
            lines.append(line)
            if len(lines) == 33:

                example = make_training_example(lines)
                # write to tfRecord file here

                lines = []


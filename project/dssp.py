def make_training_example(lines):
    """
    Takes lines read from file and created a training example.
    """
    example = {'id': lines[1].rstrip(),
               'primary': lines[3].rstrip(),
               'mask': lines[31].rstrip()}

    # pssm = []
    # for i in range(5, 26):
    #     pssm.append([float(x) for x in lines[i].split()])
    # example['pssm'] = pssm
    #
    # tertiary = []
    # for i in range(27, 30):
    #     tertiary.append([float(x) for x in lines[i].split()])
    # example['tertiary'] = tertiary

    return example


def main():
    with open('data/casp11/training_100', 'r') as raw_data:
        lines, examples = [], []
        for line in raw_data:
            lines.append(line)
            if len(lines) == 33:
                examples.append(make_training_example(lines))
                lines = []
            if len(examples) > 100:
                break

    for example in examples:
        dssp_file = example['id'][:4].lower() + '.dssp'
        with open('data/dssp/' + dssp_file, 'r') as raw_dssp:
            partial_primary, secondary = [], []
            flag = False
            for line in raw_dssp:
                if flag or ('#' in line):
                    if not flag:
                        flag = True
                        continue
                if flag:
                    if line[7:10] == '   ':
                        continue
                    p, s = line[13], line[16]
                    partial_primary.append(p)
                    secondary.append(s)
        example['partial_primary'] = ''.join(partial_primary)
        example['secondary'] = ''.join(secondary)

        with open('test.txt', 'a') as out_file:
            out_file.write(example['id'] + '\n')
            out_file.write('\n')
            out_file.write(example['primary'] + '\n')
            out_file.write('\n')
            out_file.write(example['partial_primary'] + '\n')
            out_file.write(example['secondary'] + '\n')
            out_file.write('\n')

    return


if __name__ == '__main__':
    main()

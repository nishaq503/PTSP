import tensorflow as tf

from project.model import Model


def main():

    model = Model('A', [[1]], '+', [[1]], 1)
    print(tf.__version__)

    return


if __name__ == '__main__':
    main()

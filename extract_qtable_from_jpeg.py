import argparse

from utils.qtables import save_qtable


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Gets the quantization table (qtable) out of an existing JPEG file and saves it.')
    parser.add_argument('path', help='The path of the JPEG to extract the quantization table from.')
    args = parser.parse_args()

    print(save_qtable(args.path))

#!usr/bin/python

import sys


def idf_mapper():
    for line in sys.stdin:
        line = line.strip()
        filename_word, tf_score = line.split('\t', 1)
        filename, word = filename_word.split('@', 1)
        print('{}\t{}'.format(word+ '@'+ filename, tf_score))


if __name__ == '__main__':
    idf_mapper()

import sys
import os
from string import punctuation

def mapper():

    for line in sys.stdin:
        line = line.strip()
        line = line.translate(None, punctuation)
        words = line.split()
        
        for word in words:
            word = word.lower()
            l = os.getenv('mapreduce_map_input_file','noname')
            l = l.split("/")
            filename = l[len(l) - 1]
            #print("{}\t{}\t{}".format(filename, word, 1))
            print('{}\t{}'.format(filename+'@'+word, 1))


if __name__ == "__main__":
    mapper()

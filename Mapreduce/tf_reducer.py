#!usr/bin/python
import sys


def tfreduce():
    current_file = None
    filename = None
    current_word = None
    word = None
    current_count = 0
    number_of_terms = 0
    tmp = {}
    for line in sys.stdin:
        line = line.strip()
        filename_word, count = line.split('\t', 1)
        filename, word = filename_word.split('@', 1)
        try:
            count = int(count)
        except ValueError:
            continue
      
        if current_file == filename:
            # replace 1 by count if you use a combiner !(but make sure to insert the entire block in the try/except
            number_of_terms += 1
            if current_word == word:
                current_count += count
            else:
                if current_word:
                    tmp[current_word] = current_count
                current_word = word
                current_count = count
        else:
            tmp[current_word] = current_count
            if current_file:
                for key in tmp:
                    print('{}\t{}'.format(key + '@' + current_file, tmp[key]/float(number_of_terms)))
            current_file = filename
            current_word = word
            current_count = count
            tmp = {}
            number_of_terms = 1
    
    # printing results for the last file
    for key in tmp:
        print('{}\t{}'.format(key + '@' + current_file, tmp[key]/float(number_of_terms)))
    print('{}\t{}'.format(current_word + '@' + current_file, current_count/float(number_of_terms)))


if __name__ == '__main__':
    tfreduce()

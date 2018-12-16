#!usr/bin/python
import sys
from math import log10

def idf_reducer():
    current_word = None
    word = None
    filename = None
    all_files =set()
    document_frequency = {}
    # The key in this dictionary has the form 'word@filename'
    tf_scores = {}
    for line in sys.stdin:
        line = line.strip()
        word_filename, tf_score = line.split('\t', 1)
        try:
            tf_score = float(tf_score)
        except ValueError:
            continue
        word, filename = word_filename.split('@', 1)

        if current_word == word:
            document_frequency[current_word] += 1
            tf_scores[current_word+'@'+filename] = tf_score
            all_files.add(filename)
        else:
            #if current_word:
            #    document_frequency[current_word] = 1
            current_word = word
            tf_scores[current_word+'@'+filename] = tf_score
            document_frequency[current_word] = 1
            all_files.add(filename)
    #tf_scores[current_word+'@'+current_file] = tf_score

    # N is the total number of documents
    N = len(all_files)
    # Compute the TF-IDF score
    for key in tf_scores:
        key_df = key.split('@', 1)[0]
        tf_idf_score = tf_scores[key] * log10(N/float(document_frequency[key_df]))
        print('{}\t{}'.format(key, tf_idf_score))
if __name__ == '__main__':
    idf_reducer()

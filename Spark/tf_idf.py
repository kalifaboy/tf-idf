import pyspark
from os import path
from string import punctuation
from math import log10

table = {ord(char) : None for char in punctuation}

def tokenize(s):
    s = s.lower()
    s = s.translate(table)
    return s.split()

text_files = sc.wholeTextFiles("./data/*.txt")
text_files = text_files.map(lambda x: (path.basename(x[0]), x[1]))
# Compute the total number of documents
number_of_docs = text_files.count()
# Tokenize text
tokenized_text = text_files.mapValues(lambda x: tokenize(x))
file_word_count = tokenized_text.map(lambda x: (x[0], len(x[1])))
# Flat tokenization 
tokenized_text_flat = text_files.flatMapValues(lambda x: tokenize(x))
combine_tokenized_text = tokenized_text_flat.map(lambda x: (x, 1)).reduceByKey(lambda x, y: x + y)
combine-tokenized_text = combine_tokenized_text.map(lambda x: (x[0][0], (x[0][1], x[1])))
# Term frequency RDD
tf_rdd = combine_tokenized_text.join(file_word_count)
tf_rdd = tf_rdd.map(lambda x: (x[1][0][0], (x[0], x[1][0][1]/float(x[1][1]))))
# Document frequency RDD
df_rdd = tokenized_text_flat.map(lambda x: (x[1], x[0])).distinct()
df_rdd = df_rdd.map(lambda x: (x[0], 1)).reduceByKey(lambda x,y: x + y)
# TF-IDF
tf_idf = tf_rdd.join(df_rdd)
tf_idf = tf_idf.map(lambda x: ((x[0], x[1][0][0]), x[1][0][1] * log10(number_of_docs/float(x[1][1]))))
tf_idf.take(10)

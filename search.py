#!/usr/bin/python
import re
import nltk
import sys
import getopt
import pickle

def deserialize_dictionary(dictionary_file_path):
    with open(dictionary_file_path) as f:
        dictionary = pickle.load(f)
    return dictionary

def get_posting_for_term(term, dictionary, postings_file_path):
    (offset, length) = dictionary[term]
    
    with open(postings_file_path, 'r') as f:
        f.seek(offset)
        posting_byte = f.read(length)
        posting_list = pickle.loads(posting_byte)
    return posting_list

def transform_postfix(postfix_expression):
    dictionary = deserialize_dictionary(dictionary_file)
    operators = {'AND', 'OR', 'NOT'}
    for i in range(len(postfix_expression)):
        if postfix_expression[i] not in operators:
            postfix_expression[i] = \
                get_posting_for_term(postfix_expression[i], dictionary, postings_file)
    return postfix_expression

def usage():
    print "usage: " + sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results"

dictionary_file = postings_file = file_of_queries = output_file_of_results = None
	
try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-d':
        dictionary_file  = a
    elif o == '-p':
        postings_file = a
    elif o == '-q':
        file_of_queries = a
    elif o == '-o':
        file_of_output = a
    else:
        assert False, "unhandled option"

if dictionary_file == None or postings_file == None or file_of_queries == None or file_of_output == None :
    usage()
    sys.exit(2)

print(transform_postfix(['price', 'level', 'OR']))
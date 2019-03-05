#!/usr/bin/python
import re
import nltk
import sys
import os
import getopt
import linecache
import pickle
from nltk.stem.porter import PorterStemmer

def index(input_directory, output_file_dictionary, output_file_postings):
    files = os.listdir(input_directory)
    dictionary = {'': set()}

    #Store the terms in a dictionary of {word: set containing the postins}
    for file in files:
        terms_in_file = process_file(input_directory, file)
        dictionary[''].add(int(file)) #store all postings with a key of empty string

        for term in terms_in_file:
            if term not in dictionary:
                dictionary[term] = {int(file)}
            else:
                dictionary[term].add(int(file))
    
    process_dictionary(dictionary, output_file_dictionary, output_file_postings)

    #for testing
    dictionary = deserialize_dictionary(output_file_dictionary)
    posting = get_posting_for_term('price', dictionary, output_file_postings)
    print(posting)

def process_dictionary(dictionary, output_file_dictionary, output_file_postings):
    dictionary_to_be_saved = save_to_postings(dictionary, output_file_postings)
    
    with open(output_file_dictionary, 'w') as fr:
        pickle.dump(dictionary_to_be_saved, fr)
    
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

def save_to_postings(dictionary, output_file_postings):
    dictionary_to_be_saved = {}
    current_pointer = 0
    with open(output_file_postings, 'w') as f:
        for k, v in dictionary.iteritems():
            sorted_posting = sorted(list(v))
            f.write(pickle.dumps(sorted_posting))
            byte_size = f.tell() - current_pointer
            dictionary_to_be_saved[k] = (current_pointer, byte_size)
            current_pointer = f.tell()
    
    return dictionary_to_be_saved

'''
process a file and return a list of all terms in that file
'''
def process_file(input_directory, file):
        line_num = 1
        line = linecache.getline(os.path.join(input_directory, file), line_num)
        all_terms = []
        while line != '':
            all_terms.extend(process_line(line))
            line_num += 1
            line = line = linecache.getline(os.path.join(input_directory, file), line_num)
        
        return all_terms
            
'''
process a line and return a list of all terms in that line
'''
def process_line(line):
    sentences = nltk.sent_tokenize(line)
    all_terms = []
    for sentence in sentences:
        all_terms.extend(process_sentence(sentence))
    
    return all_terms

'''
process a sentence and return a list of all terms in that sentence
Stemmer is done using NLTK's PorterStemmer
'''
def process_sentence(sentence):
    words = nltk.word_tokenize(sentence)
    all_terms = []
    stemmer = PorterStemmer()
    for word in words:
        all_terms.append(process_word(word, stemmer))
    
    return all_terms

'''
stems a word with the required stemmer
'''
def process_word(word, stemmer):
    #PorterStemmer internally already does case folding for us
    #https://www.nltk.org/_modules/nltk/stem/porter.html
    #so we only need to stem and don't need to worry about case-folding
    return stemmer.stem(word)


def usage():
    print "usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file"

input_directory = output_file_dictionary = output_file_postings = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
    
for o, a in opts:
    if o == '-i': # input directory
        input_directory = a
    elif o == '-d': # dictionary file
        output_file_dictionary = a
    elif o == '-p': # postings file
        output_file_postings = a
    else:
        assert False, "unhandled option"
        
if input_directory == None or output_file_postings == None or output_file_dictionary == None:
    usage()
    sys.exit(2)

index(input_directory, output_file_dictionary, output_file_postings)
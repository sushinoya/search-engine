#!/usr/bin/python
import re
import nltk
import sys
import os
import getopt
import linecache
from nltk.stem.porter import PorterStemmer
import Dictionary

def index(input_directory, output_file_dictionary, output_file_postings):
    files = os.listdir(input_directory)
    dictionary = Dictionary(output_file_dictionary)
    postings = Postings(output_file_postings)

    all_terms = []
    for file in files:
        all_terms.extend(process_file(input_directory, file))
    
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
    words = nltk.word_tokenize()
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

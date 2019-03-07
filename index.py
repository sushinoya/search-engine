#!/usr/bin/python
import re
import nltk
import sys
import os
import getopt
import linecache
import pickle
from utils import deserialize_dictionary, save_to_disk, clock_and_execute, generate_occurences_file, stem

def index(input_directory, output_file_dictionary, output_file_postings):
    files = os.listdir(input_directory)
    dictionary = {'': set()}

    # Store the terms in a dictionary of {word: set containing the postins}
    for file in files:
        terms_in_file = process_file(input_directory, file)
        dictionary[''].add(int(file)) #store all postings with a key of empty string

        for term in terms_in_file:
            if term not in dictionary:
                dictionary[term] = {int(file)}
            else:
                dictionary[term].add(int(file))
    
    # Generates a file of human readable postings and occurences. Maily used for debugging
    # Each line is of the format: `word`: num_of_occurences -> `[2, 10, 34, ...]` (postings list)
    generate_occurences_file(dictionary)

    # Saves the postings file and dictionary file to disk
    process_dictionary(dictionary, output_file_dictionary, output_file_postings)

def process_dictionary(dictionary, output_file_dictionary, output_file_postings):
    dictionary_to_be_saved = save_to_postings_and_generate_dictionary(dictionary, output_file_postings)
    save_to_disk(dictionary_to_be_saved, output_file_dictionary)

def save_to_postings_and_generate_dictionary(dictionary, output_file_postings):
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
Process a file and return a list of all terms in that file
'''
def process_file(input_directory, file):
    with open(os.path.join(input_directory, file), 'r') as content_file:
        text = content_file.read().replace('\n', ' ')
        return process_text(text)


'''
Process a text and return a list of all terms in that text
'''
def process_text(text):
    sentences = nltk.sent_tokenize(text)
    all_terms = []
    for sentence in sentences:
        all_terms.extend(process_sentence(sentence))
    
    return all_terms

'''
Process a sentence and return a list of all terms in that sentence
Stemmer is done using NLTK's PorterStemmer
'''
def process_sentence(sentence):
    words = nltk.word_tokenize(sentence)
    return [process_word(word) for word in words]


'''
Stems a word with the required stemmer
'''
def process_word(word): 
    return stem(word).lower()

def usage():
    print "usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file"

input_directory = output_file_dictionary = output_file_postings = None

if __name__ == "__main__":
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

    print("Indexing...")
    clock_and_execute(index, input_directory, output_file_dictionary, output_file_postings)

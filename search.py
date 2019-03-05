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

'''
postfix: a list of post expression
parses the postfix_expression and get the result of the search engine
'''
def parse_postfix(postfix_expression):
    postfix_expression = transform_postfix(postfix_expression)
    operators = {'AND', 'OR', 'NOT'}
    stack = []
    for token in postfix_expression:
        if token in operators:
            operand_1 = stack.pop()
            if token == 'NOT':
                result = evaluate_not(operand_1)
            elif token == 'AND':
                operand_2 = stack.pop()
                result = evaluate_and(operand_1, operand_2)
            else:
                operand_2 = stack.pop()
                result = evaluate_or(operand_1, operand_2)
            stack.append(result)
        else:
            stack.append(token)
    return stack.pop()

#get all the postings
def get_superset():
    dictionary = deserialize_dictionary(dictionary_file)
    return get_posting_for_term('', dictionary, postings_file)

def evaluate_not(posting):
    superset = get_superset()
    answer = []
    posting_index = 0
    superset_index = 0
    while posting_index != len(posting) and superset_index != len(superset):
        if posting[posting_index] == superset[superset_index]:
            posting_index += 1
            superset_index += 1
        elif posting[posting_index] < superset[superset_index]:
            answer.append(posting[posting_index])
            posting_index += 1
        else:
            answer.append(superset[superset_index])
            superset_index += 1
    
    while superset_index < len(superset):
        answer.append(superset[superset_index])
        superset_index += 1

    return answer


def evaluate_or(postings_1, postings_2):
    return list_union(postings_1, postings_2)

def list_union(list_1, list_2):
    answer = []
    list_1_index = 0
    list_2_index = 0
    while list_1_index != len(list_1) and list_2_index != len(list_2):
        if list_1[list_1_index] == list_2[list_2_index]:
            answer.append(list_1[list_1_index])
            list_1_index += 1
            list_2_index += 1
        elif list_1[list_1_index] < list_2[list_2_index]:
            answer.append(list_1[list_1_index])
            list_1_index += 1
        else:
            answer.append(list_2[list_2_index])
            list_2_index += 1
    
    while list_1_index < len(list_1):
        answer.append(list_1[list_1_index])
        list_1_index += 1
    
    while list_2_index < len(list_2):
        answer.append(list_2[list_2_index])
        list_2_index += 1
    
    return answer

def evaluate_and(postings_1, postings_2):
    return list_intersection(postings_1, postings_2)

def list_intersection(list_1, list_2):
    answer = []
    list_1_index = 0
    list_2_index = 0
    while list_1_index != len(list_1) and list_2_index != len(list_2):
        if list_1[list_1_index] == list_2[list_2_index]:
            answer.append(list_1[list_1_index])
            list_1_index += 1
            list_2_index += 1
        elif list_1[list_1_index] < list_2[list_2_index]:
            list_1_index += 1
        else:
            list_2_index += 1
    
    return answer
        


def usage():
    print "usage: " + sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results"





if __name__ == "__main__":
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
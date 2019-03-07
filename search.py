import re
import nltk
import sys
import getopt
import pickle
from time import time
from shunting_yard import shunting_yard
from postings_eval import evaluate_not, evaluate_or, evaluate_and
from utils import preprocess_raw_query, deserialize_dictionary, clock_and_execute, get_postings_for_term, preprocess_raw_word

'''
Replace query terms with their corresponding postings, except for 'AND', 'OR', 'NOT'

Eg. 
Input: ['A', 'B', 'AND', 'C', 'OR']
Output: [[1,3,34,46,57], [12,45,66,79,101], 'AND', [1,3,89,103,55], 'OR']

'''
def transform_postfix(postfix_expression):
    dictionary = deserialize_dictionary(dictionary_file)
    operators = {'AND', 'OR', 'NOT'}
    for i in range(len(postfix_expression)):
        if postfix_expression[i] not in operators:
            postfix_expression[i] = \
                get_postings_for_term(preprocess_raw_word(postfix_expression[i]), dictionary, postings_file)
    return postfix_expression

'''
Parses and evaluates the postfix expression and gets the result of the query
'''
def parse_and_eval_postfix(postfix_expression):
    postfix_expression = transform_postfix(postfix_expression)
    operators = 'AND', 'OR', 'NOT'
    stack = []
    for token in postfix_expression:
        if token in operators:
            operand_1 = stack.pop()
            if token == 'NOT':
                result = evaluate_not(operand_1, get_superset())
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

'''
Get the list of all the document ids
'''
def get_superset():
    dictionary = deserialize_dictionary(dictionary_file)
    return get_postings_for_term('ALL_WORDS_AND_POSTINGS', dictionary, postings_file)
    
def usage():
    print "usage: " + sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results"


# MAIN SEARCH FUNCTION
def get_postings_for_queries(file_of_queries):

    # List of queries as strings fom the query file
    queries = [line.rstrip('\n') for line in open(file_of_queries)]
    for query in queries:

        # Stems the query and normalises some terms
        preprocessed_query = preprocess_raw_query(query)

        # Converts to postfix, parses postfix and evaluates it
        output = parse_and_eval_postfix(shunting_yard(preprocessed_query))
        
        # Write the result to the output file
        with open(file_of_output, 'a') as file:
            file.write(' '.join(map(str, output)) + '\n')
    
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

    # Delete content from the output file
    with open(file_of_output, "w"):
        pass
    
    clock_and_execute(get_postings_for_queries, file_of_queries)
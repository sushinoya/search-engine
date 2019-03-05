#!/bin/bash
directory_of_documents=reuters/training
dictionary_file=dictionary.txt
postings_file=postings.txt
file_of_queries=queries.txt
output_of_results_file=queries_output.txt

python index.py -i $directory_of_documents -d $dictionary_file -p $postings_file
python search.py -d $dictionary_file -p $postings_file -q $file_of_queries -o $output_of_results_file
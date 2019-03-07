This is the README file for A0155836W-A0157691U submission

== Python Version ==

I'm (We're) using Python Version <2.7.10> for
this assignment.

== General Notes about this assignment ==

Give an overview of your program, describe the important algorithms/steps 
in your program, and discuss your experiments in general.  A few paragraphs 
are usually sufficient.

Indexing step: 
Iterate through all the training files and index all the terms in the files.
This will generate a dictionary whose {key: value} are {words: set of postings}
For each dictionary entry, sort the values into a sorted list of postings, and save the 
lists into the postings.txt file using pickle. Get the size of the byte that is written 
into the postings.txt file for each word, and in a new dictionary, reflect this piece of information. 
This new dictionary is one whose {key: value} are {words : (offset, length)}, where offset is the starting
position of the pointer to point to in the postings.txt, and lenght is the size of byte to read for each word. 
For example, we could have an entry {'bill': (10, 100)}. When we want to retrieve the postings list for 'bill', 
we will use python's seek(10) to go to position 10, and read 100 bytes of the data to retrieve the postings list
for 'bill'. Lastly, save both the new dictionary and postings to disk. 

Searching step:
Transform each query into postfix expression with shunting yard algorithm. 
For each query, replace the word with its postings list, using dictionary.txt and postings.txt
Next, evaluate each query using functions in postings_eval.py 
For skip pointers used during AND queries, simply skip by square root of the length of each list if conditions match.  

== Files included with this submission ==

List the files in your submission here and provide a short 1 line
description of each file.  Make sure your submission's files are named
and formatted correctly.
1. index.py - file for indexing the terms, and save them to dictionary.txt and postings.txt
2. dictionary.txt - the dictionary of the terms that are being indexed
3. postings.txt - the postings of the terms that are being indexed
4. search.py - file for executing the queries.
5. utils.py - file that contains some utility functions
6. shunting_yard.py - file that contains the shunting yard algorithm
7. postings_eval.py - file that contains the functions to evaluate AND, OR, NOT queries

== Statement of individual work ==

Please initial one of the following statements.

[X] I, A0155836W-A0157691U, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[ ] I, A0000000X, did not follow the class rules regarding homework
assignment, because of the following reason:

<Please fill in>

I suggest that I should be graded as follows:

<Please fill in>

== References ==
-Python documentation on its various built in libraries
-Stack overflow for various python functions
-Wikipedia shunting yard algorithm page

<Please list any websites and/or people you consulted with for this
assignment and state their role>

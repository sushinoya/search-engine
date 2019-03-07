import pickle
from time import time
import re
from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()

def preprocess_raw_word(word):
	# Stemming and Casefolding
	# In most cases stemming lowercases the words but in some special
	# cases like to, in , the, we found that both TO and to, IN and in
	# THE and the were in our dictionary, so we are going to an extra
	# step to lowercase it for certain.
	return stemmer.stem(word).lower()


index_text_preprocessing_rules = {
	# Slashes, dot, comma, dash preceeded and succeeded by a digit
	"(?P<back>\d)(\/|-|,)(?P<front>\d)": "\g<back> \g<front>",
	
	# Eg. Change suyash/shekhar to  suyash shekhar
	"(?P<back>[a-zA-Z0-9]*)\/(?P<forward>[a-zA-Z0-9]*)": "\g<back> \g<forward>"
}

def preprocess_raw_text(text):
	for regex, replacement in index_text_preprocessing_rules.items():
		text = re.sub(regex, replacement, text)
	return text

query_preprocessing_rules = {
  # Slashes, dot, comma, dash preceeded and succeeded by a digit
	"(?P<back>\d)(\/|-|,)(?P<front>\d)": " ( \g<back> OR \g<front> ) ",
	
	# Eg. Change suyash/shekhar to  ( suyash OR shekhar )
	"(?P<back>[a-zA-Z0-9]*)\/(?P<forward>[a-zA-Z0-9]*)": " ( \g<back> OR \g<forward> ) "
}

def preprocess_raw_query(query):
	for regex, replacement in query_preprocessing_rules.items():
		query = re.sub(regex, replacement, query)
	return query


#load the dictionary from dictionary_file_path using pickle
def deserialize_dictionary(dictionary_file_path):
	with open(dictionary_file_path) as f:
		dictionary = pickle.load(f)
	return dictionary

#takes in a term and dictionary, and generate the posting list
def get_postings_for_term(term, dictionary, postings_file_path):
    if term not in dictionary: 
        return []

    offset, length = dictionary[term]
    
    with open(postings_file_path, 'r') as f:
        f.seek(offset)
        posting_byte = f.read(length)
        posting_list = pickle.loads(posting_byte)
    return posting_list

#save an object to disk 
def save_to_disk(obj, file):
  	with open(file, 'w') as fr: pickle.dump(obj, fr)

def clock_and_execute(func, *args):
	start_time = time()
	ret = func(*args)
	end_time = time()
	print("Executed {}{} in {} sec." \
		.format(func.__name__, args, end_time - start_time))
	return ret

def generate_occurences_file(dictionary):
	len_dict = {word: len(v) for word, v in dictionary.items()}
	with open("occurences.txt", 'w') as f:
		for k, v in sorted(len_dict.items(), key=lambda x: -x[1]):
			f.write("{}: {} -> {}\n".format(k.ljust(15), str(v).ljust(5), sorted(list(dictionary[k]))))
    

import pickle
from time import time
from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()

def stem(word):
	return stemmer.stem(word).lower()


def deserialize_dictionary(dictionary_file_path):
	with open(dictionary_file_path) as f:
		dictionary = pickle.load(f)
	return dictionary

def get_postings_for_term(term, dictionary, postings_file_path):
    if term not in dictionary: 
        return []

    offset, length = dictionary[term]
    
    with open(postings_file_path, 'r') as f:
        f.seek(offset)
        posting_byte = f.read(length)
        posting_list = pickle.loads(posting_byte)
    return posting_list

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
    

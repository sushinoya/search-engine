import pickle
from time import time

def deserialize_dictionary(dictionary_file_path):
	with open(dictionary_file_path) as f:
		dictionary = pickle.load(f)
	return dictionary

def get_postings_for_term(term, dictionary, postings_file_path):
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

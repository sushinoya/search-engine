import pickle
from time import time

def deserialize_dictionary(dictionary_file_path):
	with open(dictionary_file_path) as f:
		dictionary = pickle.load(f)
	return dictionary

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
    

from utils import stem, deserialize_dictionary, get_postings_for_term
from shunting_yard import shunting_yard

def test_stemming():
  print(stem("U.S. BANK NET FREE RESERVES 644 MLN DLRS IN TWO WEEKS TO FEB 25, FED SAYS"))


def test_shunting_yard():
    print('Testing shunting yard:')
    actual = shunting_yard("bill OR Gates AND(vista OR XP) AND NOT mac")
    expected = ['bill', 'Gates', 'vista', 'XP',
                'OR', 'AND', 'mac', 'NOT', 'AND', 'OR']
    print(actual == expected)
    print('\n')


def test_index():
    print('Testing indexing: ')
    dictionary_file = "dictionary.txt"
    postings_file = "postings.txt"
    dictionary = deserialize_dictionary(dictionary_file)
    actual = get_postings_for_term('price', dictionary, postings_file)
    expected = [1, 5, 10]
    print(actual == expected)
    print('\n')

test_stemming()
test_shunting_yard()
test_index()

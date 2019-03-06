from utils import stem, deserialize_dictionary, get_postings_for_term
from shunting_yard import shunting_yard

def test_stemming():
  print(stem('''U.S. BANK NET FREE RESERVES 644 MLN DLRS IN TWO WEEKS TO FEB 25, FED SAYS

             U.S. BANK NET FREE RESERVES 644 MLN DLRS IN TWO WEEKS TO FEB 25, FED SAYS


             '''))
  print(stem('U.S. BANK NET FREE RESERVES 644 MLN DLRS IN TWO WEEKS TO FEB 25, FED SAYS'))
  print(stem("limited OR to"))
  print(stem('to'))
  print(stem("flavour"))
  print(stem('''
  The flavours and
  fragrances firm &lt;Naarden International N.V.>, acquired by
  Anglo-Dutch food and detergents group Unilever Plc N.V. &lt;UN.AS>
  last year, said net profits for 1986 fell 11.4 pct to 19.5 mln
  guilders.
      Naarden said earnings were hit by the fall in the value of
  both the dollar and sterling, noting the figure was in line
  with prior expectations. Net profit was 22.0 mln guilders in
  1985.
      Earnings per share fell to 4.64 guilders from 5.48 in 1985
  on turnover of 627.8 mln, down from 662.6 mln. Naarden set a
  cash dividend of 1.80 guilders, unchanged from last year but
  without last year's share option for payment.'''))

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

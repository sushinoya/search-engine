from utils import stem, deserialize_dictionary, get_postings_for_term
from shunting_yard import shunting_yard
import nltk

line_2965 = '''
GERMAN 1988 TAX CUTS RAISED BY 5.2 BILLION MARKS
  Senior officials in the West German
  coalition government said tax cuts planned for next year would
  be increased by 5.2 billion marks, in line with a pledge made
  by Finance Minister Gerhard Stoltenberg at last month's
  international monetary conference in Paris.
      Gerold Tandler, General Secretary of the Christian Social
  Union Party, detailing the cuts at a news conference also
  attended by officials from the Christian Democratic Union and
  Free Democratic Party, said all of the additional 5.2 billion
  mark reduction would represent net tax relief.
      An increase in revenue from other sources was not planned.
      The reductions will be added on to a package of tax cuts
  already planned for 1988 amounting to some nine billion marks.
      Tandler said three billion marks of the extra tax relief
  would be accounted for by reducing the rate of marginal
  increase in income tax.
      An increase in personal tax allowances would save taxpayers
  1.4 billion marks. Extra tax allowances for people whose
  children are being educated would cut 300 mln marks from the
  tax bill. A further 500 mln marks would be accounted for by
  increasing the level of special depreciations for small- and
  medium-sized companies.
      The extra fiscal measures planned for next year are part of
  a general reform of the tax system which will come into effect
  in 1990. Stoltenberg had said in Paris that part of this
  reform, which will cut taxes by a gross 44 billion marks, would
  be introduced next year, ahead of schedule.
      The West German government had come under pressure from the
  United States to stimulate its economy with tax cuts. But
  Stoltenberg said in a speech last night in Hamburg that, while
  the economy would continue to expand this year, the rate of
  growth was uncertain.
      The government said in January it was aiming for real
  growth in Gross National Product this year of 2.5 pct, but some
  economists have revised their predictions down to two or below.
      Stoltenberg said: "We remain on a course of expansion.
  Whether (this will be) under two pct, as some people believe,
  or around 2.5 pct as some others expect, or even closer to
  three pct, as the Kiel World Economic Institute forecast a few
  days ago, remains open at the moment."
  


'''

def test_stemming():
  print(stem('''U.S. BANK NET FREE RESERVES 644 MLN DLRS IN TWO WEEKS TO FEB 25, FED SAYS

             U.S. BANK NET FREE RESERVES 644 MLN DLRS IN TWO WEEKS TO FEB 25, FED SAYS


             '''))
  print(stem('U.S. BANK NET FREE RESERVES 644 MLN DLRS IN TWO WEEKS TO FEB 25, FED SAYS'))
  print(stem("limited OR to"))
  print(stem('to'))
  print(stem("flavour"))

  print(stem("month's"))

def test_tokenize():
    print(nltk.sent_tokenize(line_2965))

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


test_tokenize()
test_stemming()
# test_shunting_yard()
# test_index()


def generate_line_by_line(r):
    with open("shit.txt", 'w') as file:
        file.write('\n'.join(map(str, r)) + '\n')

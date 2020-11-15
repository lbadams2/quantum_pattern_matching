'''
test.py

Liam Adams and Alec Landow

References:
    https://www.geeksforgeeks.org/python-string-find/#:~:text=The%20find()%20method%20returns,found%20then%20it%20returns%20%2D1.
    https://www.geeksforgeeks.org/binary-decimal-vice-versa-python/
    https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
    https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-python
'''

from pattern_match import run_match
from pprint import pprint
from operator import itemgetter
from termcolor import colored

# expected: a list
def test(input_string, pattern):
    counts = run_match(input_string, pattern, True)
    print(f'input  : {input_string}')
    print(f'pattern: {pattern}')
    pprint(counts)

    expected = input_string.find(pattern)
    countsDictionary = dict(counts)
    result = int( max(counts.items(), key = itemgetter(1))[0], 2)
    print(f'Expected: {expected}')
    print(f'Result: {result}')
    if (expected == result):
        print( colored('Test Passed', 'green') )
    else:
        print( colored('Test Failed', 'red') )

    print()

if __name__ == '__main__':
    test('0000', '0')

    test('1000', '1')
    test('0100', '1')
    test('0010', '1')
    test('0001', '1')

    test('0000', '00')
    test('1000', '10')

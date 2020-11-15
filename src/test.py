'''
test.py

Liam Adams and Alec Landow

References:
    https://www.geeksforgeeks.org/python-string-find/#:~:text=The%20find()%20method%20returns,found%20then%20it%20returns%20%2D1.
    https://www.geeksforgeeks.org/binary-decimal-vice-versa-python/
    https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
    https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-python
    https://stackoverflow.com/questions/8306654/finding-all-possible-permutations-of-a-given-string-in-python
'''

from pattern_match import run_match
from pprint import pprint
from operator import itemgetter
from termcolor import colored
from itertools import permutations

pass_count = 0
fail_count = 0
total_count = 0
# expected: a list
def test(input_string, pattern):
    global pass_count
    global fail_count
    global total_count

    counts = run_match(input_string, pattern, True)
    print(f'input  : {input_string}')
    print(f'pattern: {pattern}')
    pprint(counts)

    expected = input_string.find(pattern)
    countsDictionary = dict(counts)
    result = int( max(counts.items(), key = itemgetter(1))[0], 2)
    print(f'Expected: {expected}')
    print(f'Result: {result}')

    total_count = total_count + 1
    if (expected == result):
        pass_count = pass_count + 1
        print( colored('Test Passed', 'green') )
    else:
        fail_count = fail_count + 1
        print( colored('Test Failed', 'red') )

    print()

if __name__ == '__main__':
    test('0000', '0')

    # perms = [''.join(p) for p in permutations('stack')]


    for pattern in ('0', '1'):
        test('1000', pattern)
        test('0100', pattern)
        test('0010', pattern)
        test('0001', pattern)

    for pattern in ('0', '1'):
        test('0111', pattern)
        test('1011', pattern)
        test('1101', pattern)
        test('1110', pattern)


    test('0000', '00')
    test('1000', '10')

    test('00000001', '1')
    test('00000001', '01')
    test('10000001', '1')
    test('10000001', '01')


    print(f'{fail_count} tests failed and {pass_count} tests passed '
        + f'out of {total_count} total tests')

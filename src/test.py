'''
test.py

Liam Adams and Alec Landow

References:
    https://www.geeksforgeeks.org/python-string-find/#:~:text=The%20find()%20method%20returns,found%20then%20it%20returns%20%2D1.
    https://www.geeksforgeeks.org/binary-decimal-vice-versa-python/
    https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
    https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-python
    https://stackoverflow.com/questions/8306654/finding-all-possible-permutations-of-a-given-string-in-python
    https://stackoverflow.com/questions/663171/how-do-i-get-a-substring-of-a-string-in-python
'''
# perms = [''.join(p) for p in permutations('stack')]

from pattern_match import run_match
from pprint import pprint
from operator import itemgetter
from termcolor import colored
from itertools import permutations

pass_count = 0
valid_count = 0
fail_count = 0
total_count = 0
# expected: a list
def test(input_string, pattern):
    global pass_count
    global valid_count
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
        result_substring = input_string[ result : result + len(pattern) ]

        if result_substring == pattern:
            valid_count = valid_count + 1
            print( colored('Correct Match, Unexpected Location', 'yellow') )
        else:
            fail_count = fail_count + 1
            print( colored('Test Failed', 'red') )

    print()

def test_single_char_patterns():
    test('0000', '0')

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

    test('00000001', '1')
    test('10000001', '1')

def test_two_char_patterns():
    for input_string in ('0011', '0010', '1100', '0100', '0000'):
        test(input_string, '00')

    for input_string in ('1000', '0100', '0010'):
        test(input_string, '10')

    for input_string in ('0100', '0010', '0001'):
        test(input_string, '01')

    for input_string in ('1100', '0110', '0011', '1111'):
        test(input_string, '11')

    test('00000000', '00')
    test('00000011', '00')

    test('00000001', '01')
    test('10000001', '01')

    test('10000001', '10')
    test('10000000', '10')

    test('11111111', '11')
    test('10000011', '11')

def test_three_char_patterns():
    for input_string in ('0001', '1000', '0000'):
        test(input_string, '000')

    for input_string in ('1010', '0101'):
        test(input_string, '101')

    for input_string in ('1100', '1101', '0110', '1110'):
        test(input_string, '110')

    for input_string in ('0110', '0111', '0011', '1011'):
        test(input_string, '011')

    for input_string in ('1100', '0110', '0011', '1111'):
        test(input_string, '11')

    test('00000000', '000')
    test('00000011', '000')

    test('00000001', '001')
    test('10000001', '001')

    test('10000001', '100')
    test('10000000', '100')

    test('11111111', '111')
    test('10000111', '111')

def run_tests():
    # test_single_char_patterns()
    test_two_char_patterns()
    # test_three_char_patterns()

if __name__ == '__main__':
    for i in range(10):
        run_tests()

    print("Results:")
    print(f'\tFailed: {fail_count} tests')
    print(f'\tValid : {valid_count} tests')
    print(f'\tPassed: {pass_count} tests')
    print('\t------------------------')
    print(f'\tTotal: {total_count} tests')
    print('\t------------------------')
    num_matches = valid_count + pass_count
    print(f'\tMatches         : {num_matches} tests')
    print('\tFail Percentage : {fail_perc:.2f} %'
        .format(fail_perc = fail_count / total_count * 100))
    print('\tMatch Percentage: {match_perc:.2f} %'
        .format(match_perc = num_matches / total_count * 100))

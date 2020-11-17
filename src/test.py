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
    https://www.w3schools.com/python/ref_string_format.asp
    https://docs.python.org/3/library/re.html
    https://docs.python.org/3/library/re.html#match-objects
    https://docs.python.org/3/howto/regex.html
    https://stackoverflow.com/questions/1419046/normal-arguments-vs-keyword-arguments
'''
# perms = [''.join(p) for p in permutations('stack')]
import re

from pattern_match import run_match
from pprint import pprint
from operator import itemgetter
from termcolor import colored
from itertools import permutations
from random import randrange

from sys import argv

pass_count = 0
valid_count = 0
fail_count = 0
total_count = 0

use_ibm = False
oracle_type = ''
diffuser_type = ''

alphabet = None

def test(input_string, pattern):
    global pass_count
    global valid_count
    global fail_count
    global total_count

    global use_ibm
    global oracle_type
    global diffuser_type

    print('alphabet = ' + ''.join(alphabet))
    counts = run_match(
        input_string,
        pattern,
        is_test_run = True,
        use_ibm = use_ibm,
        oracles = oracle_type,  # 'many' or 'single'
        diffuser = diffuser_type, # 'gates' or 'matrix'
        alphabet = alphabet
    )

    print(f'input  : {input_string}')
    print(f'pattern: {pattern}')
    pprint(counts)

    pattern = re.sub('\*', '.', pattern)

    expected = re.search(pattern, input_string).start() #input_string.find(pattern)
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
        result_substring_matchObject = re.search(pattern, result_substring)
        if len(result_substring) == len(pattern) and result_substring_matchObject != None:
            valid_count = valid_count + 1
            print( colored('Correct Match, Unexpected Location', 'yellow') )
        else:
            fail_count = fail_count + 1
            print( colored('Test Failed', 'red') )

    print()

def random_string(alphabet, N):
    alphabet_len = len(alphabet)
    rand_string = ''
    for _ in range(N):
        char = alphabet[ randrange(alphabet_len) ]
        rand_string += str(char)
    return rand_string

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

    for input_string in ('0010', '1100', '0100', '1000', '0100', '0010'):
        test(input_string, '10')


    test('00000000', '00')
    test('00000011', '00')

    test('00000001', '01')
    test('10000001', '01')

    test('10000001', '10')
    test('10000000', '10')

    test('11111111', '11')
    test('10000011', '11')

def test_three_char_patterns():
    for input_string in ('00011111', '10001111', '00001111'):
        test(input_string, '000')

    for input_string in ('10101111', '01011111'):
        test(input_string, '101')

    for input_string in ('11001111', '11011111', '01101111', '11101111'):
        test(input_string, '110')


    for input_string in ('01101111', '01111111', '00111111', '10111111'):
        test(input_string, '011')


    for input_string in ('11101111', '01111111', '11111111'):
        test(input_string, '111')

    test('00000000', '000')
    test('00000011', '000')

    test('00000001', '001')
    test('10000001', '001')

    test('10000001', '100')
    test('10000000', '100')

    test('11111111', '111')
    test('10000111', '111')

def test_wildcard_patterns():
    test('0000', '*')

    test('1000', '*')
    test('0100', '*')
    test('0010', '*')
    test('0001', '*')
    test('0111', '*')
    test('1011', '*')
    test('1101', '*')
    test('1110', '*')

    test('00000001', '*')
    test('10000001', '*')

    for input_string in ('0011', '0010', '1100', '0100', '0000', '1000', '0100', '0010'):
        test(input_string, '*0')
        test(input_string, '**')

    for input_string in ('11000000', '11010000', '01100000', '11100000'):
        test(input_string, '11*')
        test(input_string, '***')

    for input_string in ('01101111', '01111111', '00111111', '10111111'):
        test(input_string, '*11')
        test(input_string, '*1*')

def test_random_pattern_and_input(use_wildcards):
    N = 8
    M = 2
    alphabet = '01'

    num_random_tests = 20

    while num_random_tests > 0:
        input_string = random_string(alphabet, N)

        if use_wildcards:
            pattern = random_string(alphabet + '*', M)
            regex_pattern = re.sub('\*', '.', pattern)
        else:
            pattern = random_string(alphabet, M)
            regex_pattern = pattern

        if re.search(regex_pattern, input_string):
            test(input_string, pattern)
            num_random_tests -= 1

def test_exact_matches():
    global alphabet
    alphabet = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')

    # test('aaab', 'b')
    # test('aaba', 'b')
    # test('abaa', 'b')
    # test('baaa', 'b')
    #
    # for char in alphabet:
    #     test('abcdefgh', char)
    #
    for pattern_length in (2, 3, 4, 5):
        for i in range(len(alphabet) - (pattern_length - 1) ):
            pattern = ''.join( alphabet[i : i + pattern_length] )
            print(f"pattern: {pattern}")
            test('abcdefgh', pattern)



def run_tests():
    if len(argv) == 1:
        test_wildcard_patterns()
        test_single_char_patterns()
        test_two_char_patterns()
        test_three_char_patterns()
        test_random_pattern_and_input(False)
        test_random_pattern_and_input(True)

    elif argv[1] == '*':
        test_wildcard_patterns()

    elif argv[1] == 'exact':
        test_exact_matches()

    elif argv[1] == 'random' or argv[1] == '?' or argv[1] == 'rand':
        if len(argv) == 3 and argv[2] == '*':
            test_random_pattern_and_input(True)
        else:
            test_random_pattern_and_input(False)

    elif re.search('\d+', argv[1]):
        num_chars_in_pattern = int(argv[1])

        if num_chars_in_pattern == 1:
            test_single_char_patterns()
        elif num_chars_in_pattern == 1:
            test_single_char_patterns()
        elif num_chars_in_pattern == 2:
            test_two_char_patterns()
        elif num_chars_in_pattern == 3:
            test_three_char_patterns()
    else:
        print("Invalid Input")
        print("python test.py [ \* | <A NUMBER> ]")


if __name__ == '__main__':
    use_ibm = True

    test_count = 1
    test_results = list()
    for this_oracle_type in ('many', 'single'):
        for this_diffuser_type in ('gates', 'matrix'):
            oracle_type = this_oracle_type
            diffuser_type = this_diffuser_type

            pass_count = 0
            valid_count = 0
            fail_count = 0
            total_count = 0

            test_result = list()

            header_lines = list()
            header_lines.append('================================')
            header_lines.append(f'Test {test_count}:')
            header_lines.append(f'\tOracle Type: {oracle_type}')
            header_lines.append(f'\tDiffuser Type: {diffuser_type}')
            header = '\n'.join(header_lines)
            print(header)

            for i in range(1):
                run_tests()

            test_result.append(header)

            test_result.append("Results:")
            test_result.append(f'\tFailed: {fail_count} tests')
            test_result.append(f'\tValid : {valid_count} tests')
            test_result.append(f'\tPassed: {pass_count} tests')
            test_result.append('\t------------------------')
            test_result.append(f'\tTotal: {total_count} tests')
            test_result.append('\t------------------------')

            num_matches = valid_count + pass_count
            test_result.append(f'\tMatches         : {num_matches} tests')
            test_result.append('\tFail Percentage       : {fail_perc:.2f} %'
                .format(fail_perc = fail_count / total_count * 100))
            test_result.append('\tMatch Percentage      : {match_perc:.2f} %'
                .format(match_perc = num_matches / total_count * 100))
            test_result.append('\tFirst Match Percentage: {first_match_perc:.2f} %'
                .format(first_match_perc = pass_count / total_count * 100))

            test_results.append( '\n'.join(test_result) )
            test_count += 1

    for test_result in test_results:
        print(test_result)

'''
oracles.py

Liam Adams and Alec Landow

Creates oracles for each letter of the alphabet

References
    https://www.geeksforgeeks.org/iterate-over-characters-of-a-string-in-python/

'''

from qiskit import quantum_info
import numpy as np

alphabet = ('0', '1')


def generate_oracles(s, input_string, pattern_length, debug):
    oracles = dict()

    for pattern_char in alphabet:
        oracles[pattern_char] = list()
        N = len(input_string)
        M = pattern_length

        for i in range( N - M + 1 ):
            pattern_char_oracle_matrix = np.identity( int( 2**s ) )
            # print(f'{input_string[i]} =? {pattern_char}')
            if input_string[i] == pattern_char:
                pattern_char_oracle_matrix[i, i] = -1

                if debug:
                    print(f"Oracle for '{pattern_char}'[{i}]")
                    print(pattern_char_oracle_matrix)
                    print()
                oracles[pattern_char].append( quantum_info.Operator( pattern_char_oracle_matrix ) )

    wildcard_oracle_matrix = np.multiply( -1, np.identity( int( 2**s ) ) )
    # print(wildcard_oracle_matrix)
    oracles['*'] = quantum_info.Operator( wildcard_oracle_matrix )
    return oracles

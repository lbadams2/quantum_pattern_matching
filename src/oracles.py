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


def generate_oracles(s, input_string, pattern_length):
    oracles = dict()

    for pattern_char in alphabet:
        pattern_char_oracle_matrix = np.identity( int( 2**s ) )
        # TODO: Imitate tensor products
        N = len(input_string)
        M = pattern_length
        for i in range( 2**s ):
            # print(f'{input_string[i]} =? {pattern_char}')
            if input_string[i] == pattern_char:
                pattern_char_oracle_matrix[i, i] = -1

        # print(pattern_char_oracle_matrix)
        # print()
        oracles[pattern_char] = quantum_info.Operator( pattern_char_oracle_matrix )

    wildcard_oracle_matrix = np.multiply( -1, np.identity( int( 2**s ) ) )
    # print(wildcard_oracle_matrix)
    oracles['*'] = quantum_info.Operator( wildcard_oracle_matrix )
    return oracles

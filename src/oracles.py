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

        N = len(input_string)
        M = pattern_length
        for i in range( N - M + 1 ):
            if input_string[i] == pattern_char:
                pattern_char_oracle_matrix[i, i] = -1

        oracles[pattern_char] = quantum_info.Operator( pattern_char_oracle_matrix )

    wildcard_oracle_matrix = np.multiply( -1, np.identity( int( 2**s ) ) )
    oracles['*'] = quantum_info.Operator( wildcard_oracle_matrix )
    return oracles

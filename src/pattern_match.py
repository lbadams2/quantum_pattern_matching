'''
pattern_match

Liam Adams and Alec Landow

main program to run the Mateus/Omar pattern match algorithm

Example:
N = 10
M = 2

1 / (sqrt(10 - 2 + 1)) = 1 / 3

(1 / 3) * (
      |1, .., 10> 
    + |2, .., 10> 
    + |3, .., 10> 
    + |4, .., 10> 
    + |5, .., 10> 
    + |6, .., 10>
    + |7, .., 10>
    + |8, 9, 10>
    + |9, 10>
    + |10>
)

'''

import math

from oracles import oracles

def add_pattern_char_state(qc):
    pass

# create walsh hadamard of N-M+1 qubits with N - M + 1 = 2^s
# need walsh hadamard on s qubits
# figure 2 on page 4
def create_initial_state(qc, M):
    # Apply H gates to each of the s qubits in the first pattern char state
    # foreach (M - 1): add_pattern_char_state()
    # sequentially entangle each character
    # each character represented by s qubits, s is number of bits in index
    for i in range(M-1):
        add_pattern_char_state(qc)


def pattern_match(qc):
    # 1. Choose r from [ 0 .. floor(sqrt(N - M + 1)) ] <-- random selection
    # 2. create_initial_state()
    # 3.
    for i in range(1, r + 1, 1):
        # j: index of a char in the pattern
        # a. Choose j from [1, M] <-- random selection
        # b. Apply Q_(p_j) to the set of s qubits that represent pattern char j
        # c. Apply Diffusion Operator to the entire state psi
        
    pass


if __name__ == '__main__':
    # get input string
    # get pattern

    number_of_iterations = math.sqrt(N)
    for q in (number_of_iterations):
        pattern_match(qc)
    
    # create initial state
    # get the oracle corresponding to each letter in the pattern



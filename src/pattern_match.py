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

References
    https://qiskit.org/documentation/stubs/qiskit.circuit.ControlledGate.html
    https://stackoverflow.com/questions/61286794/is-there-an-anti-control-gate-in-qiskit

'''

import math

from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.circuit.library.standard_gates import XGate
from qiskit import Aer, IBMQ, execute
from oracles import generate_oracles

'''
Example for s = 3:
https://algassert.com/quirk#circuit=%7B%22cols%22%3A%5B%5B%22H%22%2C%22H%22%2C%22H%22%5D%2C%5B%22%E2%80%A2%22%2C1%2C1%2C%22X%22%5D%2C%5B1%2C%22%E2%80%A2%22%2C1%2C1%2C%22X%22%5D%2C%5B1%2C1%2C%22%E2%80%A2%22%2C1%2C1%2C%22X%22%5D%2C%5B1%2C1%2C%22%E2%97%A6%22%2C1%2C1%2C%22X%22%5D%2C%5B1%2C%22%E2%97%A6%22%2C%22%E2%80%A2%22%2C1%2C1%2C%22X%22%5D%2C%5B1%2C%22%E2%97%A6%22%2C%22%E2%80%A2%22%2C1%2C%22X%22%5D%2C%5B%22%E2%97%A6%22%2C%22%E2%80%A2%22%2C%22%E2%80%A2%22%2C1%2C1%2C%22X%22%5D%2C%5B%22%E2%97%A6%22%2C%22%E2%80%A2%22%2C%22%E2%80%A2%22%2C1%2C%22X%22%5D%2C%5B%22%E2%97%A6%22%2C%22%E2%80%A2%22%2C%22%E2%80%A2%22%2C%22X%22%5D%5D%7D

       / -[ H ]-----------------
qr_p0 {  -[ H ]-----------------
       \ -[ H ]-----------------
       / -----------------------
qr_p1 {  -----------------------
       \ -----------------------

     ...

'''
qubits_for_pattern_chars = dict()

# The control state is a list of 0's and 1's that encodes whether a 0 or a 1
#   will activate the control for the i_th qubit in the control state string
def _build_control_state(num_control_qubits):
    control_state = ''
    for i in range(num_control_qubits - 1):
        control_state = control_state + '1'

    control_state = control_state + '0'
    return control_state


def _add_pattern_char_state(qc, i, s):
    new_qubits = QuantumRegister(s)
    qc.add_register(new_qubits)
    qubits_for_pattern_chars[i] = new_qubits

    previous_qubits = qubits_for_pattern_chars[i - 1]

    # Entangle previous qubits with the new qubits
    for j in range(s):
        qc.cx(previous_qubits[j], new_qubits[j])

    # Encode the order of the pattern char locations
    for upper_qubit_index in range(s - 1, -1, -1):
        for lower_qubit_index in range(s - 1, upper_qubit_index - 1, -1):
            num_control_qubits = s - upper_qubit_index

            acx = XGate().control(
                num_ctrl_qubits = num_control_qubits,
                ctrl_state = _build_control_state(num_control_qubits)
            )

            acx_qargs = list(previous_qubits[upper_qubit_index : s])
            acx_qargs.append(new_qubits[lower_qubit_index])

            qc.append(acx, qargs = acx_qargs)

    qc.barrier()


# create walsh hadamard of N-M+1 qubits with N - M + 1 = 2^s
# need walsh hadamard on s qubits
# figure 2 on page 4
def create_initial_state(qc, s, M):
    qubits_for_pattern_chars[0] = QuantumRegister(s)
    qc.add_register(qubits_for_pattern_chars[0])
    qc.h(qubits_for_pattern_chars[0])

    # Apply H gates to each of the s qubits in the first pattern char state
    # foreach (M - 1): add_pattern_char_state()
    # sequentially entangle each character
    # each character represented by s qubits, s is number of bits in index
    for i in range(1, M + 1):
        _add_pattern_char_state(qc, i, s)


def pattern_match(qc):
    r = 0 # TODO: remove placeholder
    # 1. Choose r from [ 0 .. floor(sqrt(N - M + 1)) ] <-- random selection
    # 2. create_initial_state()
    # 3.
    for i in range(1, r + 1, 1):
        # j: index of a char in the pattern
        # a. Choose j from [1, M] <-- random selection
        # b. Apply Q_(p_j) to the set of s qubits that represent pattern char j
        # c. Apply Diffusion Operator to the entire state psi
        pass

    pass


if __name__ == '__main__':
    # get input string
    # get pattern
    input_string = 'ccabccccc'
    N = len(input_string)

    pattern = 'ab'
    M = len(pattern)

    # N - M + 1 = 2^s
    s = math.ceil( math.log2(N - M + 1) ) # round up if N - M + 1 is not a power of 2

    qc = QuantumCircuit()
    oracles = generate_oracles(s, input_string)

    create_initial_state(qc, s, M)

    # run ~sqrt(N) times
    number_of_iterations = math.ceil( math.sqrt( math.pow(s, 2) ) )
    for q in range(number_of_iterations):
        pattern_match(qc)


    # qc.draw(output = 'mpl', plot_barriers = False, filename = "test1.png")
    print( qc )

    # get the oracle corresponding to each letter in the pattern

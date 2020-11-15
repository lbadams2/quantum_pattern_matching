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
    https://pynative.com/python-random-randrange/#:~:text=Use%20randint()%20when%20you,number%20from%20an%20exclusive%20range.
    https://stackoverflow.com/questions/339007/how-to-pad-zeroes-to-a-string
    https://stackoverflow.com/questions/40999973/how-to-pad-a-numeric-string-with-zeros-to-the-right-in-python

'''

import math

from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit import Aer, IBMQ, execute
from qiskit import quantum_info

from qiskit.circuit.library.standard_gates import XGate

from oracles import generate_oracles
from random import randint
from sys import argv

import numpy as np
import pprint



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
simulatorBackend = Aer.get_backend('qasm_simulator')

debug = False

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
    for i in range(1, M):
        _add_pattern_char_state(qc, i, s)

def diffuser_old(qc, oracles, M, s):
    for j in range(0, len(qubits_for_pattern_chars)):
        qc.h( qubits_for_pattern_chars[j] )

    diffuser_matrix = np.identity( int( 2**(s * M) ) )
    diffuser_matrix[0, 0] = -1
    qubit_start_index = 0
    qubit_stop_index  = qubit_start_index + (s * M)
    qc.unitary(
        quantum_info.Operator( diffuser_matrix ),
        range( qubit_start_index, qubit_stop_index ),
        label = " U'"
    )

    for j in range(0, len(qubits_for_pattern_chars)):
        qc.h( qubits_for_pattern_chars[j] )

# Derived From Qiskit
def diffuser(qc, M, s):
    nqubits = M * s

    # Apply transformation |s> -> |00..0> (H-gates)
    for qubit in range(nqubits):
        qc.h(qubit)
    # Apply transformation |00..0> -> |11..1> (X-gates)
    for qubit in range(nqubits):
        qc.x(qubit)
    # Do multi-controlled-Z gate
    qc.barrier()
    qc.h(nqubits-1)
    qc.mct(list(range(nqubits-1)), nqubits-1)  # multi-controlled-toffoli
    qc.h(nqubits-1)
    qc.barrier()
    # Apply transformation |11..1> -> |00..0>
    for qubit in range(nqubits):
        qc.x(qubit)
    # Apply transformation |00..0> -> |s>
    for qubit in range(nqubits):
        qc.h(qubit)

def pattern_match(qc, oracles, pattern, M, s):
    # j: index of a char in the pattern
    # a. Choose j randomly from [1, M]
    j = randint( 0, len(pattern) - 1 )
    pattern_char = pattern[j]

    for single_position_oracle in oracles[pattern_char]:
        # b. Apply Q_(p_j) to the set of s qubits that represent pattern char j
        qubit_start_index = j * s
        qubit_stop_index  = qubit_start_index + s
        qc.unitary(
            single_position_oracle,
            range( qubit_start_index, qubit_stop_index ),
            label = f" ['{pattern[j]}' Oracle]"
        )
        qc.barrier()

        # c. Apply Diffusion Operator to the entire state psi
        # diffuser(qc, oracles, M, s)
        diffuser(qc, M, s)

        qc.barrier()

    return

def run_match(input_string, pattern, is_test_run):
    debug = not is_test_run
    if input_string == None:
        input_string = argv[1]

    if pattern == None:
        pattern = argv[2]

    if input_string == "" or input_string == None:
        input_string = '01'.ljust( 2**3, '0' )
    padded_length = 2**( math.ceil(math.log2(len(input_string))) )
    input_string = input_string.ljust( padded_length, '0' )
    if debug:
        print( f'input_string = {input_string}' )
    N = len(input_string)

    if pattern == "" or pattern == None:
        pattern = '1'
    M = len(pattern)

    if debug:
        print( f'pattern = {pattern}' )

    # N - M + 1 = 2^s
    s = math.ceil( math.log2(N - M + 1) ) # round up if N - M + 1 is not a power of 2

    if debug:
        print(f's = {s}')

    qc = QuantumCircuit()
    oracles = generate_oracles( s, input_string, len(pattern), debug )

    create_initial_state(qc, s, M)

    # run ~sqrt(N) times
    number_of_iterations = 1 # math.ceil( math.sqrt( math.pow(s, 2) ) )
    if debug:
        print(f'number_of_iterations = {number_of_iterations}')
    for q in range(number_of_iterations):
        pattern_match( qc, oracles, pattern, M, s )

    classicalRegisters = ClassicalRegister(s)
    qc.add_register(classicalRegisters)
    qc.measure( qubits_for_pattern_chars[0], classicalRegisters )

    if debug:
        # qc.draw(output = 'mpl', plot_barriers = True, filename = "test2.png")
        print( qc )

    backend = simulatorBackend
    # backend = IBMQBackend
    shots = 2**13
    job = execute(qc, backend = backend, shots = shots)
    results = job.result()
    counts = results.get_counts()

    return counts

if __name__ == '__main__':
    counts = run_match(None, None, False)

    pprint.pprint(counts)

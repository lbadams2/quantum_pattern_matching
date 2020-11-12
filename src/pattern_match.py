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

def diffuser(qc, oracles, s):
    # qc.h( qubits_for_pattern_chars[0] )
    for qubit_group in qubits_for_pattern_chars:
        qc.h( qubit_group )

    diffuser_matrix = np.identity( int( 2**s ) )
    diffuser_matrix[0, 0] = -1
    qubit_start_index = 0
    qubit_stop_index  = qubit_start_index + s
    qc.unitary(
        oracles['*'], # quantum_info.Operator( diffuser_matrix ),
        range( qubit_start_index, qubit_stop_index ),
        label = " U'"
    )

    qc.h( qubits_for_pattern_chars[0] )


def pattern_match(qc, oracles, pattern, s):
    # j: index of a char in the pattern
    # a. Choose j randomly from [1, M]
    j = randint( 0, len(pattern) - 1 )
    # print(f'j = {j}')

    # b. Apply Q_(p_j) to the set of s qubits that represent pattern char j
    qubit_start_index = j * s
    qubit_stop_index  = qubit_start_index + s
    pattern_char = pattern[j]
    qc.unitary(
        oracles[ pattern_char ],
        range( qubit_start_index, qubit_stop_index ),
        label = f" ['{pattern[j]}' Oracle]"
    )
    qc.barrier()

    # c. Apply Diffusion Operator to the entire state psi
    diffuser(qc, oracles, s)

    qc.barrier()

    return


if __name__ == '__main__':
    # get input string
    # get pattern
    input_string = '010'.ljust( 2**3, '0' ) # '010'.zfill( 2**4 )
    padded_length = 2**( math.ceil(math.log2(len(input_string))) )
    input_string = input_string.ljust( padded_length, '0' )
    print( f'input_string = {input_string}' )
    N = len(input_string)

    pattern = '010'
    M = len(pattern)
    print( f'pattern = {pattern}' )

    # N - M + 1 = 2^s
    s = math.ceil( math.log2(N - M + 1) ) # round up if N - M + 1 is not a power of 2
    print(f's = {s}')

    qc = QuantumCircuit()
    oracles = generate_oracles( s, input_string, len(pattern) )

    create_initial_state(qc, s, M)

    # run ~sqrt(N) times
    number_of_iterations = math.ceil( math.sqrt( math.pow(s, 2) ) )
    print(f'number_of_iterations = {number_of_iterations}')
    for q in range(number_of_iterations):
        pattern_match( qc, oracles, pattern, s )

    classicalRegisters = ClassicalRegister(s)
    qc.add_register(classicalRegisters)
    qc.measure( qubits_for_pattern_chars[0], classicalRegisters )

    qc.draw(output = 'mpl', plot_barriers = True, filename = "test2.png")
    print( qc )

    backend = simulatorBackend
    # backend = IBMQBackend
    shots = 2**13
    job = execute(qc, backend = backend, shots = shots)
    results = job.result()
    counts = results.get_counts()

    pprint.pprint(counts)

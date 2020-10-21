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
from oracles import oracles

'''
Example for s = 3:

       / -[ H ]-----------------
qr_p0 {  -[ H ]-----------------
       \ -[ H ]-----------------
       / -----------------------
qr_p1 {  -----------------------
       \ -----------------------

     ...

'''
qubits = dict()

def _build_control_state(num_control_qubits):
    control_state = ''
    for i in range(num_control_qubits - 1):
        control_state = control_state + '1'

    # print(f"number of control qubits: {len(previous_qubits[upper_qubit_index : s])}")
    control_state = control_state + '0'
    print(control_state)
    return control_state


def add_pattern_char_state(qc, i, s):
    new_qubits = QuantumRegister(s)
    qc.add_register(new_qubits)
    qubits[f'qr_p{i}'] = new_qubits

    previous_qubits = qubits[f'qr_p{i - 1}']

    # Entangle previous qubits with the new qubits
    for j in range(s):
        qc.cx(previous_qubits[j], new_qubits[j])

    # Encode the order of the pattern char locations
    for upper_qubit_index in range(s - 1, -1, -1):
        for lower_qubit_index in range(s - 1, upper_qubit_index - 1, -1):
            num_control_qubits = s - upper_qubit_index
            print(f'num_control_qubits: {num_control_qubits}')
            acx = XGate().control(num_ctrl_qubits = num_control_qubits, ctrl_state = _build_control_state(num_control_qubits) )
            print(f"acx control qubits: {acx.num_ctrl_qubits}")
            print(f'len(previous_qubits[upper_qubit_index : s]) = {len(previous_qubits[upper_qubit_index : s])}')
            print(f'upper_qubit_index = {upper_qubit_index}')
            # print(f"test qargs length {len([ previous_qubits[upper_qubit_index : s], new_qubits[lower_qubit_index] ])}")
            acx_qargs = list(previous_qubits[upper_qubit_index : s])
            acx_qargs.append(new_qubits[lower_qubit_index])
            print(f"test len: {acx_qargs}")
            qc.append(acx, qargs = acx_qargs)
            # qc.mcx(previous_qubits[j : s], new_qubits[k])

    qc.barrier()


# create walsh hadamard of N-M+1 qubits with N - M + 1 = 2^s
# need walsh hadamard on s qubits
# figure 2 on page 4
def create_initial_state(qc, s, M):
    qubits['qr_p0'] = QuantumRegister(s)
    qc.add_register(qubits['qr_p0'])
    qc.h(qubits['qr_p0'])

    # Apply H gates to each of the s qubits in the first pattern char state
    # foreach (M - 1): add_pattern_char_state()
    # sequentially entangle each character
    # each character represented by s qubits, s is number of bits in index
    for i in range(1, M + 1):
        add_pattern_char_state(qc, i, s)


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
    create_initial_state(qc, s, M)

    qc.draw(output = 'mpl', plot_barriers = False, filename = "test1.png")

    # run ~sqrt(N) times
    number_of_iterations = math.ceil( math.sqrt( math.pow(s, 2) ) )
    for q in range(number_of_iterations):
        pattern_match(qc)

    # create initial state
    # get the oracle corresponding to each letter in the pattern

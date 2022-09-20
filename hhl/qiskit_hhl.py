from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer
from qiskit.quantum_info import Statevector
from qiskit.algorithms.linear_solvers.hhl import HHL

import numpy as np

def qiskit_HHL(A,b):

    backend = Aer.get_backend('aer_simulator')
    #qiskit HHL 코드를 불러옴
    hhl = HHL(quantum_instance=backend)
    #A, b에 대해서 HHL 회로를 구성
    solution = hhl.solve(A, b)
    #만들어진 회로를 그림으로 저장
    solution.state.draw("mpl").savefig("./outputs/HHL_circuit_qiskit.png")
    #연산된 상태를 상태 벡터의 형태로 결과를 얻음
    naive_sv = Statevector(solution.state).data
    #qubit수를 확인
    num_qubit = solution.state.num_qubits
    #상태 벡터에서 필요한 상태만을 골라서 저장함
    naive_full_vector = np.array([naive_sv[2**(num_qubit-1)+i] for i in range(len(b))])
    #실수 부분만 취함
    naive_full_vector = np.real(naive_full_vector)
    #얻어진 벡터를 normalize하여 반환
    normalized_result = naive_full_vector/np.linalg.norm(naive_full_vector)

    constant = b/(A @ normalized_result)
    constant = (constant[0]+constant[1])/2
    constant = np.mean(constant)

    print('<Qiskit_HHL>')
    print('Normalized Qiskit Answer : {0}'.format(normalized_result))
    print('Un-normalized Qiskit Answer : {0}'.format(normalized_result * constant))
    print('Normalize Constant: ' ,constant)

    return [normalized_result,normalized_result * constant]
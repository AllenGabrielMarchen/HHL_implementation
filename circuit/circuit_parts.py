#circuit_parts.py

from qiskit.circuit.library.arithmetic.exact_reciprocal import ExactReciprocal
from qiskit.circuit.library.arithmetic.piecewise_chebyshev import PiecewiseChebyshev
from qiskit import QuantumCircuit, QuantumRegister,Aer
import numpy as np

def qft_dagger(n_l):

# <qft를 구현하는 과정에 있어서 SWAP gate에 대한 참고사항>

# SWAP 게이트를 걸어주는 목적은 qiskit은 qubit을 반대방향으로 읽기 때문임.
# 하지만, SWAP 게이트를 위와 같은 이유로 걸어주게 된다고 하면, 
# HHL 알고리즘 상에서 Eigeninversion 단계에서 문제가 생기게 됨. 
# 즉, Eigeninversion에서는 SWAP이 된 상태를 인지하지 못하고 연산을 실시하여 잘못된 연산이 나오게 됨.

    """n-qubit QFTdagger the first n qubits in circ"""
    nl_rg = QuantumRegister(n_l, "l")
    qc = QuantumCircuit(nl_rg)
    # Don't forget the Swaps!
    #QFT의 역연산은 곧 QFT_dagger임을 기억하자.
        
    for j in reversed(range(n_l)):
        qc.h(j)
        for m in reversed(range(j)):
                qc.cp(-np.pi/float(2**(j-m)), m, j)
    qc.name = "QFT†"
    #display(qc.draw(output = 'mpl'))
    return qc
    
def QPE(n_l,n_b,CU):
    #circuit initialization for HHL
    nl_rg = QuantumRegister(n_l, "l")
    nb_rg = QuantumRegister(n_b, "b")
    #QuantumRegister(size=None, name=None, bits=None) 
    qc = QuantumCircuit(nl_rg,nb_rg)
    #display(qc.draw(output = 'mpl'))
    qc.h(nl_rg)
    qc.barrier(nl_rg[:]+nb_rg[:])
    for l in range(n_l):
        for power in range(2**(l)):
            qc.append(CU, [nl_rg[l],nb_rg[0],nb_rg[1]]) 
            #첫번째 큐비트는 2^0번, 이후 2^n꼴로 돌아가게 설계됨.
            #https://qiskit.org/documentation/stubs/qiskit.circuit.ControlledGate.html append의 예제.
            #즉, append의 첫번째 인자는 gate, 두번쨰 인자의 첫번째 요소는 control qubit, 이후 인자의 요소는 target qubit.

    qc.barrier(nl_rg[:]+nb_rg[:])
    qc.append(qft_dagger(n_l),nl_rg[:])
    qc.barrier(nl_rg[:]+nb_rg[:])
    qc.name = "QPE"
    #display(qc.draw(output = 'mpl'))
    return qc
    
def QPE_dagger(n_l,n_b,CU):
    qc = QPE(n_l,n_b,CU)
    qc = qc.inverse()
    #여기서 inverse함수는 모든 rotation 각도까지도 반대로 입력해줌을 확인하였음.
    #QPE dagger는 그저, QPE의 역과정이라고 생각하면 된다. 단, 각도는 반대방향이어야 함.
    #따라서 여기서 inverse함수를 이용하여 QPE의 역과정, 즉, QPE dagger를 실시하였음
    qc.name = 'QPE†'
    return qc

def Eigenvalue_inversion(n_l,delta,chevyshev = False):

    #Chevyshev 근사를 이용한 풀이방법.
    #Qiskit에서 제공한 HHL 알고리즘 상에서는 Chevyshev 근사를 이용한 부분이 있었다.
    #일단 Chevyshev 근사를 이용하는 경우, 기존 Taylor 근사보다 훨씬 빠르게 급수에 수렴한다는 장점이 있다.
    #참고 문헌 : https://freshrimpsushi.github.io/posts/chebyshev-expansion/
    #여기서는 위의 표현한 cos(theta)에 대한 표현을 Chevyshev근사를 이용해 theta값을 알아내겠다는 접근방법이다.
    #하지만, 근사결과가 좋지 못하다는 점 때문에 Chevyshev 근사를 이용하는 대신에 직접 exact한 theta값을 알아내는 ExactReciprocal을 이용하였다.

    if chevyshev == True:
        print("Maybe using Chevyshev approximation is not accurate.")
        #Using Chebychev Approx. (not recommended!)
        nl_rg = QuantumRegister(n_l, "l")
        na_rg = QuantumRegister(n_l, "a")
        nf_rg = QuantumRegister(1, "f")
        qc = QuantumCircuit(nl_rg, na_rg, nf_rg)

        f_x, degree, breakpoints, num_state_qubits = lambda x: np.arcsin(1 / x), 2, [1,2,3,4], n_l
        #degree : 함수를 polynomial로 근사할 떄, 최고차항 정의
        #breakpoints는 구간을 나누는 느낌. : 근사를 할 떄, 다항식을 어떤 구간에서 나눠서 사용할 지
        #l : eigenvalue를 표현
        #f : rotation
        #a : ancila
        pw_approximation = PiecewiseChebyshev(f_x, degree, breakpoints, num_state_qubits)
        pw_approximation._build()
        qc.append(pw_approximation,nl_rg[:]+[nf_rg[0]]+na_rg[:]) #range(nl*2+1))
        qc.name = 'Chevyshev_inversion'
        return qc

    else:
        qc = ExactReciprocal(n_l, delta, neg_vals = True)
        qc.name = 'Reciprocal_inversion'
        return qc
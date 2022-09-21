#setup.py

import numpy as np
from scipy.linalg import expm

from qiskit.extensions import UnitaryGate
from qiskit.circuit.add_control import add_control
from qiskit import Aer

import circuit
import hhl
import tools

#참고 논문 :Low Complexity Quantum Matrix Inversion A기gorithm for non-Hermitian Matrices

def main(A,b,backend,shots,t,n_l,delta):

    #Check if Hermitian
    if np.allclose(A,A.T) == False:
        print("Given A matrice is not Hermitian.")
        print("Given Matrices will be transformed into Hermitian formation.")
        A = np.vstack((np.hstack((np.zeros_like(A),A)),np.hstack((A.T, np.zeros_like(A))))) # Hermitian의 꼴로 바꿈
        b = np.hstack((b,np.zeros_like((np.shape(A)[0]-np.shape(b)[0],1))))

    #A의 shape와 동일한 zero array를 생성하고, A의 왼쪽에 배치, horizontal 방향도 마찬가지.

    i = complex(0,1) #complex(real part, imaginary part)
    U = expm(i*A*t) #여기서 A가 행렬로 주어졌기 때문에, 행렬을 exp에 올리기 위해서는 expm이라는 scipy 패키지가 필요함.
    U_gate = UnitaryGate(U) #위에서 구성한 U라는 행렬로써 Unitary gate를 구성할 수 있음. (4*4) 행렬
    CU = add_control(U_gate,1,ctrl_state=None, label="CU") 
    #CU라는 게이트 이름을 label에 저장
    #control 되는 경우의 state를 지정 -> 해당사항 없음
    #두번째 인자는 컨트롤 큐빗의 개수를 지정함.
    n_b = int(np.log2(U.shape[0])) 
    #Ax =b의 꼴이고, b는 4*1의 shape이므로, A의 행의 개수와 동일함. 따라서, U의 행렬의 행의 개수와 동일함.
    #행의 개수에 log2를 취하면 필요한 n_b의 값을 구할 수 있음.

    My_HHL_result = hhl.My_HHL(CU,b,n_l,n_b,backend,delta,shots,A,details = True,chevyshev = False)
    print("\n")
    qiskit_result = hhl.qiskit_HHL(A,b,backend)
    print("\n")
    classical_result = hhl.classical_HHL(A,b)
    print("\n")

    #For normalized answer
    print("<Un - normalized Case Comparision>")
    print('Qiskit Error : {0}'.format(np.linalg.norm(qiskit_result[1]-classical_result[1])))
    print('My HHL Error : {0}'.format(np.linalg.norm(My_HHL_result[1]-classical_result[1])))
    print("\n")

    print("<Normalized Case Comparision>")
    print('Qiskit Error : {0}'.format(np.linalg.norm(qiskit_result[0]-classical_result[0])))
    print('My HHL Error : {0}'.format(np.linalg.norm(My_HHL_result[0]-classical_result[0])))


if __name__ == "__main__":
    
    #setups
    A = np.array([[2,-1],[1,4]]) #non-Hermitian인 경우의 행렬에 대한 저장
    b = np.array([1,1]) 
    backend = Aer.get_backend('aer_simulator')
    shots = 8192

    t = np.pi*2/16
    n_l = 3 #QPE 상에서 n_ㅣ는 하다마드로 초기화 되는 부분 
    delta = 1/16*(2**(n_l-1))

    main(A,b,backend,shots,t,n_l,delta)
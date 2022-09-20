from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
import numpy as np

import circuit as circ
import tools 

def My_HHL(CU,b,n_l,n_b,backend,delta,shots,A,details = True,chevyshev = False):
    #b_sol = np.hstack((b,np.zeros_like((np.shape(A)[0]-np.shape(b)[0],1))))

    #circuit initialization
    n_f = 1
    nb = int(np.log2(b.shape))
    nl_rg = QuantumRegister(n_l, "l")
    nb_rg = QuantumRegister(n_b, "b")
    na_rg = QuantumRegister(n_l, "a")
    nf_rg = QuantumRegister(n_f, "f")
    
    cf = ClassicalRegister(n_f, "classical_f")
    cb = ClassicalRegister(n_b, "classical_b")

    qc = QuantumCircuit(nf_rg,nl_rg, nb_rg, na_rg, cf, cb)
    
    qc.isometry(b/np.linalg.norm(b), list(range(nb)), None)
    #qc.h(nb_rg[0])
    qc.barrier(nf_rg,nl_rg,nb_rg)

    
    if details == True:
        qc = qc.compose(circ.QPE(n_l,n_b,CU),nl_rg[:]+nb_rg[:]) 
        qc = qc.compose(circ.Eigenvalue_inversion(n_l,delta,chevyshev),[nl_rg[2]]+[nl_rg[1]]+[nl_rg[0]]+nf_rg[:])
        qc = qc.compose(circ.QPE_dagger(n_l,n_b,CU),nl_rg[:]+nb_rg[:])
        qc.barrier(nf_rg[:]+nl_rg[:]+nb_rg[:])
        qc.measure(nf_rg,cf)
        qc.measure(nb_rg,cb)
        answer = circ.measurement(qc,n_l,n_b,CU,backend,shots)
        qc.draw(output = 'mpl').savefig('./outputs/qc_HHL')

    else:
        qc.append(circ.QPE(n_l,n_b,CU),nl_rg[:]+nb_rg[:])
        qc.append(circ.Eigenvalue_inversion(n_l),[nl_rg[2]]+[nl_rg[1]]+[nl_rg[0]]+nf_rg[:])
        qc.append(circ.QPE_dagger(n_l,n_b,CU),nl_rg[:]+nb_rg[:])
        qc.barrier(nf_rg[:]+nl_rg[:]+nb_rg[:])
        qc.measure(nf_rg,cf)
        qc.measure(nb_rg,cb)
        answer = circ.measurement(qc,n_l,n_b,CU,backend,shots)
        qc.draw(output = 'mpl').savefig('./outputs/qc_HHL')

    #Obtaining Normalized answer
    normalized_result = tools.normalize_vector(answer, n_b)
    
    #Obtaining Real Answer
    constant = b/(A @ normalized_result)
    constant = (constant[0]+constant[1])/2
    constant = np.mean(constant)

    print('<My_HHL>')
    print('Normalized Answer : {0}'.format(normalized_result)) 
    print('Un-normalized Answer : {0}'.format(normalized_result * constant))
    print('Normalize Constant: ' ,constant)

    return [normalized_result,normalized_result * constant]
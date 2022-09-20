from qiskit.algorithms.linear_solvers.numpy_linear_solver import NumPyLinearSolver
import numpy as np

def classical_HHL(A,b):
    
    sol = NumPyLinearSolver().solve(A, b)
    sol_state = sol.state
    norm_state = sol_state/np.linalg.norm(sol_state)

    print('<Classical case using Numpy>')

    if np.shape(b)[0] == 2:
        sol_state = np.pad(sol_state,(2,0))
        norm_state = np.pad(norm_state,(2,0))

    print('Un-normalized Classical Numpy answer : {0}'.format(sol_state,(2,0)))
    print('Normalized Classical Numpy answer : {0}'.format(norm_state,(2,0)))
    
    return [norm_state,sol_state]

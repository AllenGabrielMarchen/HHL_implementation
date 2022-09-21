#measurement.py

from qiskit import QuantumCircuit, transpile, assemble
from qiskit.visualization import plot_histogram

def measurement(qc,n_l,n_b,CU,backend,shots):
    
    t = transpile(qc, backend)
    qobj = assemble(t, shots=shots)
    results = backend.run(qobj).result()
    answer = results.get_counts()    
    plot_histogram(answer, title="Output Histogram").savefig('./outputs/output_histogram.png',facecolor='#eeeeee')

    return answer
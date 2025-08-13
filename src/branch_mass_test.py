import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from .penrose_model import noise_model_mass, noise_model_const
from .utils import safe_transpile

def branch_mass_circuit(m, time_slices=20):
    n = 1 + m
    qc = QuantumCircuit(n, 1)
    qc.h(0)
    for a in range(1, n):
        qc.cx(0, a)  # attach ancillas to |1> branch
    qc.barrier()
    for _ in range(time_slices):
        for a in range(1, n):
            qc.id(a)  # noise acts on ancillas only
    qc.barrier()
    for a in range(1, n):
        qc.cx(0, a)
    qc.h(0); qc.measure(0, 0)
    return qc

def x_expect_from_counts(counts):
    shots = sum(counts.values())
    p0 = counts.get('0', 0) / shots
    p1 = counts.get('1', 0) / shots
    return p0 - p1

def run_branch_mass(m_list, shots=1500, time_slices=25, k=0.02, alpha=1.0, p_const=0.01):
    backend = AerSimulator(method="automatic")
    x_mass, x_const = [], []
    for m in m_list:
        tqc = safe_transpile(branch_mass_circuit(m, time_slices))
        res = backend.run(tqc, noise_model=noise_model_mass(m, k, alpha), shots=shots).result()
        x_mass.append(x_expect_from_counts(res.get_counts()))
        res2 = backend.run(tqc, noise_model=noise_model_const(p_const), shots=shots).result()
        x_const.append(x_expect_from_counts(res2.get_counts()))
    return np.array(x_mass), np.array(x_const)

def plot_branch(m_list, x_mass, x_const, outpath):
    plt.figure(figsize=(7,5))
    plt.plot(m_list, x_const, marker='o', label='Constant dephasing')
    plt.plot(m_list, x_mass,  marker='s', label='Branch-mass dephasing')
    plt.xlabel('Branch mass m (ancillas on |1> branch)'); plt.ylabel('<X> on control')
    plt.title('Branch-dependent decoherence'); plt.grid(True); plt.legend(); plt.tight_layout()
    plt.savefig(outpath, dpi=180)
    plt.close()

if __name__ == "__main__":
    m_list = [0,2,4,6,8,10,12]
    x_mass, x_const = run_branch_mass(m_list, shots=1500, time_slices=25, k=0.02, alpha=1.0, p_const=0.01)
    plot_branch(m_list, x_mass, x_const, "results/branch_mass.png")
    print("Saved results/branch_mass.png")

import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from .penrose_model import noise_model_mass, noise_model_const
from .utils import safe_transpile

def ghz_circuit(n, time_slices=20):
    qc = QuantumCircuit(n, n)
    qc.h(0)
    for i in range(n - 1):
        qc.cx(0, i + 1)
    qc.barrier()
    for _ in range(time_slices):
        for q in range(n):
            qc.id(q)
    qc.barrier()
    for q in range(n):
        qc.h(q)
    qc.measure(range(n), range(n))
    return qc

def parity_from_counts(counts):
    shots = sum(counts.values())
    s = 0
    for b, c in counts.items():
        s += c if (b.count('1') % 2 == 0) else -c
    return s / shots

def run_ghz(n_list, shots=1000, time_slices=20, k=0.02, alpha=2.0, p_const=0.01):
    backend = AerSimulator(method="automatic")
    vis_mass, vis_const = [], []
    for n in n_list:
        tqc = safe_transpile(ghz_circuit(n, time_slices))
        res = backend.run(tqc, noise_model=noise_model_mass(n, k, alpha), shots=shots).result()
        vis_mass.append(parity_from_counts(res.get_counts()))
        res2 = backend.run(tqc, noise_model=noise_model_const(p_const), shots=shots).result()
        vis_const.append(parity_from_counts(res2.get_counts()))
    return np.array(vis_mass), np.array(vis_const)

def plot_ghz(n_list, vis_mass, vis_const, outpath):
    plt.figure(figsize=(7,5))
    plt.plot(n_list, vis_const, marker='o', label='Constant dephasing')
    plt.plot(n_list, vis_mass,  marker='s', label='Mass-dependent dephasing')
    plt.xlabel('Qubits in GHZ (n)'); plt.ylabel('Parity visibility')
    plt.title('GHZ parity vs n'); plt.grid(True); plt.legend(); plt.tight_layout()
    plt.savefig(outpath, dpi=180)
    plt.close()

if __name__ == "__main__":
    n_list = [2,4,6,8,10]
    vis_mass, vis_const = run_ghz(n_list, shots=1000, time_slices=20, k=0.02, alpha=2.0, p_const=0.01)
    plot_ghz(n_list, vis_mass, vis_const, "results/ghz_parity.png")
    print("Saved results/ghz_parity.png")

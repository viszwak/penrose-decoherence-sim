import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from .penrose_model import noise_model_mass, noise_model_const
from .utils import safe_transpile

def oracle_all_ones(n):
    qc = QuantumCircuit(n, name='Oracle')
    qc.mcx(list(range(n-1)), n-1)         # mark |11..1>
    return qc.to_gate()

def grover_circuit(n, iters=3):
    qc = QuantumCircuit(n, n)
    qc.h(range(n))
    O = oracle_all_ones(n)
    for _ in range(iters):
        qc.append(O, range(n))
        qc.h(range(n)); qc.append(O, range(n)); qc.h(range(n))  # simple diffusion
        for q in range(n): qc.id(q)                             # idle slice
    qc.measure(range(n), range(n))
    return qc.decompose(reps=5)  # expand mcx into supported gates

def run_grover(n_list, iters_list, shots=1200, k=0.0015, alpha=2.0, p_const=0.002):
    backend = AerSimulator(method="automatic")
    succ_mass, succ_const = {}, {}
    for n in n_list:
        succ_mass[n], succ_const[n] = [], []
        for it in iters_list:
            tqc = safe_transpile(grover_circuit(n, it))
            res = backend.run(tqc, noise_model=noise_model_mass(n, k, alpha), shots=shots).result()
            c = res.get_counts()
            succ_mass[n].append(c.get('1'*n, 0)/shots)
            res2 = backend.run(tqc, noise_model=noise_model_const(p_const), shots=shots).result()
            c2 = res2.get_counts()
            succ_const[n].append(c2.get('1'*n, 0)/shots)
    return succ_mass, succ_const

def plot_grover(n_list, iters_list, succ_mass, succ_const, outpath):
    plt.figure(figsize=(7,5))
    for n in n_list:
        plt.plot(iters_list, succ_const[n], marker='o', label=f'Const p, n={n}')
        plt.plot(iters_list, succ_mass[n],  marker='s', label=f'Mass dep, n={n}')
    plt.xlabel('Grover iterations'); plt.ylabel('Success probability (|11..1>)')
    plt.title('Grover success vs depth'); plt.grid(True); plt.legend(); plt.tight_layout()
    plt.savefig(outpath, dpi=180)
    plt.close()

if __name__ == "__main__":
    n_list, iters_list = [3,4,5], list(range(1,8))
    succ_mass, succ_const = run_grover(n_list, iters_list, shots=1200, k=0.0015, alpha=2.0, p_const=0.002)
    plot_grover(n_list, iters_list, succ_mass, succ_const, "results/grover_results.png")
    print("Saved results/grover_results.png")

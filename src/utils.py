import numpy as np
from qiskit import transpile

def set_seed(seed=7):
    np.random.seed(seed)

def safe_transpile(qc):
    # Keep 'id' gates and avoid targeting a device that might drop them.
    return transpile(qc, optimization_level=0)

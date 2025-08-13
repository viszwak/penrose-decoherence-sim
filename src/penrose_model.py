import math
from qiskit_aer.noise import NoiseModel, phase_damping_error

def p_mass(m: float, k: float = 0.02, alpha: float = 2.0) -> float:
    """Mass-dependent dephasing probability p(m) = 1 - exp(-k m^alpha)."""
    return 1.0 - math.exp(-k * (m ** alpha))

def noise_model_mass(m: float, k: float = 0.02, alpha: float = 2.0) -> NoiseModel:
    nm = NoiseModel()
    nm.add_all_qubit_quantum_error(phase_damping_error(p_mass(m, k, alpha)), ['id'])
    return nm

def noise_model_const(p_const: float = 0.01) -> NoiseModel:
    nm = NoiseModel()
    nm.add_all_qubit_quantum_error(phase_damping_error(p_const), ['id'])
    return nm

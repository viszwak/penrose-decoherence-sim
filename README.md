# Penrose Decoherence Simulation

This repository contains simulations of **gravity-induced quantum state reduction** based on the Penrose model, including both **mass-dependent** and **constant dephasing** cases. Implementations are provided for GHZ states, branch-mass tests, and Grover's algorithm using Qiskit.

## Quick Start

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run all experiments via the CLI orchestrator
python -m src.main --exp all

# Run individual experiments
python src/ghz_test.py
python src/branch_mass_test.py
python src/grover_test.py

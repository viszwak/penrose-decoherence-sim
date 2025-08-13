# Quantum Penrose Sim — Modular Version (Correct)

This is the promised **modular** repo with both standalone scripts and a CLI orchestrator,
matching the structure we discussed.

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m src.main --exp all          # runs all experiments
# or run individually:
python src/ghz_test.py
python src/branch_mass_test.py
python src/grover_test.py
```
Figures are saved to `results/`.

## Layout
- `src/penrose_model.py` — mass-dependent & constant dephasing models
- `src/ghz_test.py` — GHZ parity vs qubit count (standalone runnable)
- `src/branch_mass_test.py` — branch-dependent decoherence (standalone runnable)
- `src/grover_test.py` — Grover success vs depth (standalone runnable)
- `src/main.py` — CLI orchestrator
- `notebooks/Penrose_Patterns.ipynb` — original Colab notebook (if provided)
- `results/` — output figures

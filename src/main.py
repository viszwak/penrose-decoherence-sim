import argparse
from pathlib import Path
from .utils import set_seed
from .ghz_test import run_ghz, plot_ghz
from .branch_mass_test import run_branch_mass, plot_branch
from .grover_test import run_grover, plot_grover

def ensure(path): Path(path).mkdir(parents=True, exist_ok=True)

def main():
    parser = argparse.ArgumentParser(description="Run Penrose mass-dependent decoherence simulations")
    parser.add_argument("--exp", choices=["ghz","branch","grover","all"], default="all", help="Which experiment(s) to run")
    parser.add_argument("--shots", type=int, default=1000, help="Shots per configuration")
    parser.add_argument("--seed", type=int, default=7, help="RNG seed")
    args = parser.parse_args()

    set_seed(args.seed)
    ensure("results")

    if args.exp in ("ghz","all"):
        n_list = [2,4,6,8,10]
        vis_mass, vis_const = run_ghz(n_list, shots=args.shots, time_slices=20, k=0.02, alpha=2.0, p_const=0.01)
        plot_ghz(n_list, vis_mass, vis_const, "results/ghz_parity.png")
        print("Saved results/ghz_parity.png")

    if args.exp in ("branch","all"):
        m_list = [0,2,4,6,8,10,12]
        x_mass, x_const = run_branch_mass(m_list, shots=max(args.shots,1200), time_slices=25, k=0.02, alpha=1.0, p_const=0.01)
        plot_branch(m_list, x_mass, x_const, "results/branch_mass.png")
        print("Saved results/branch_mass.png")

    if args.exp in ("grover","all"):
        nL, itL = [3,4,5], list(range(1,8))
        succ_mass, succ_const = run_grover(nL, itL, shots=max(args.shots,1200), k=0.0015, alpha=2.0, p_const=0.002)
        plot_grover(nL, itL, succ_mass, succ_const, "results/grover_results.png")
        print("Saved results/grover_results.png")

if __name__ == "__main__":
    main()

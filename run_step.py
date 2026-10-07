"""Command-line launcher for the Data Mining Project local workflow.

Supports three modes:
  1. verify   : check dataset paths, imports, and env configuration.
  2. setup    : (re)apply the notebook local-setup patches.
  3. jupyter  : start jupyter notebook in the project root.

Examples:
  python run_step.py verify
  python run_step.py setup --dry-run
  python run_step.py jupyter
"""
import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def cmd_verify(_args):
    from src.config import DATASET_DIR, check_dataset, dataset_path, STEPCASE, SUPPORT_FILES

    print("=" * 60)
    print("Project root  :", PROJECT_ROOT)
    print("Dataset dir   :", DATASET_DIR)
    print("-" * 60)

    ok = check_dataset(("business", "review", "tip"))
    print("-" * 60)

    for name, p in SUPPORT_FILES.items():
        print(f"  [{'OK' if p.exists() else 'MISSING'}] {name:20s} {p}")
    print("-" * 60)

    for num, step in STEPCASE.items():
        nbs = list(step.glob("*.ipynb"))
        backups = list(step.glob("*.original"))
        print(f"  Step {num}: {len(nbs)} notebook(s), {len(backups)} backup(s) in {step}")

    try:
        import pandas
        import numpy
        import nltk
        import matplotlib
        import seaborn
        print("-" * 60)
        print("[OK] Core packages (pandas/numpy/nltk/matplotlib/seaborn) importable")
    except ImportError as e:
        print(f"[WARN] Missing package: {e}. Run: pip install -r requirements.txt")
        ok = False

    print("=" * 60)
    return 0 if ok else 2


def cmd_setup(args):
    import setup_notebooks
    old_argv = sys.argv[:]
    new_args = ["setup_notebooks.py"]
    if args.dry_run:
        new_args.append("--dry-run")
    if args.step:
        new_args.append(f"--step={args.step}")
    sys.argv = new_args
    try:
        setup_notebooks.main()
        return 0
    finally:
        sys.argv = old_argv


def cmd_jupyter(_args):
    import subprocess
    return subprocess.call([sys.executable, "-m", "notebook", "--notebook-dir", str(PROJECT_ROOT)])


def main():
    parser = argparse.ArgumentParser(description="Data-Mining Project Local Runner")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("verify", help="Verify environment, dataset files, and folders.")

    setup_p = sub.add_parser("setup", help="(Re)patch notebooks for local execution.")
    setup_p.add_argument("--dry-run", action="store_true")
    setup_p.add_argument("--step", type=int, choices=[1, 2, 3, 4, 5], help="Only patch this step.")

    sub.add_parser("jupyter", help="Launch Jupyter Notebook at project root.")

    args = parser.parse_args()
    mapping = {"verify": cmd_verify, "setup": cmd_setup, "jupyter": cmd_jupyter}
    return mapping[args.command](args)


if __name__ == "__main__":
    sys.exit(main() or 0)

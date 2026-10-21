"""Run Lab 2 analyses in dependency order. Maintainer: Thanh."""
import bootstrap  # noqa: F401

from pathlib import Path
import runpy

from load_data import ROOT


SCRIPTS = [
    "b1_acf_pacf.py",
    "b2_white_noise.py",
    "b3_decomposition.py",
    "b4a_missing.py",
    "b4b_outliers.py",
    "b5_visualization.py",
]


def main():
    source_dir = ROOT / "src"
    for filename in SCRIPTS:
        path = source_dir / filename
        if not path.is_file():
            raise FileNotFoundError(f"Analysis script is missing: {path}")
        print(f"\n{'=' * 76}\nRunning {filename}\n{'=' * 76}")
        runpy.run_path(str(path), run_name="__main__")
    print("\nLab 2 is complete. Figures are in docs/lab2/figures/ and processed "
          "data are in data/processed/.")


if __name__ == "__main__":
    main()

"""Generate portfolio-ready numerical summaries and figures."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from thermofluids import generate_all_figures, problem1, problem2, problem3_design, problem3_parametric, to_dict


def main() -> int:
    figures_dir = ROOT / "figures"
    results_dir = ROOT / "results"
    figures_dir.mkdir(exist_ok=True)
    results_dir.mkdir(exist_ok=True)

    first_case = problem1()
    evaporator = problem2()
    double_pipe = problem3_design()
    sensitivity = problem3_parametric(
        D=double_pipe.D_m,
        L=double_pipe.L_m,
        m_values=np.linspace(0.002, 0.004, 21),
    )
    generate_all_figures(figures_dir)

    summary = {
        "project": "Computational Thermofluids: Heat Exchanger and Boiler Modeling",
        "shell_and_tube_case": to_dict(first_case),
        "r134a_evaporator_case": to_dict(evaporator),
        "double_pipe_design": to_dict(double_pipe),
    }
    (results_dir / "heat_exchanger_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    with (results_dir / "double_pipe_sensitivity.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["m_dot", "Tco_K", "Tho_K", "Q_W", "dp_Pa"])
        writer.writeheader()
        writer.writerows(sensitivity)

    print(json.dumps(summary["double_pipe_design"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

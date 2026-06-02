"""Regression tests for the reusable heat-exchanger model."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from thermofluids import lmtd_counterflow, problem1, problem3_design


class HeatExchangerTests(unittest.TestCase):
    def test_equal_terminal_differences_return_limit(self) -> None:
        self.assertAlmostEqual(lmtd_counterflow(20.0, 20.0), 20.0)

    def test_shell_and_tube_area_is_positive(self) -> None:
        result = problem1()
        self.assertGreater(result.area, 0.0)
        self.assertGreater(result.correction_factor, 0.0)
        self.assertLessEqual(result.correction_factor, 1.0)

    def test_double_pipe_design_meets_pressure_constraint(self) -> None:
        result = problem3_design()
        self.assertAlmostEqual(result.dp_cold_Pa, 15000.0, delta=25.0)
        self.assertGreater(result.L_m, 0.0)


if __name__ == "__main__":
    unittest.main()

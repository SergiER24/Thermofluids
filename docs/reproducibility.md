# Reproducibility Guide

## Portable Workflow

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/generate_results.py
python -m unittest discover -s tests -v
```

Generated artifacts:

- `results/heat_exchanger_summary.json`
- `results/double_pipe_sensitivity.csv`
- `figures/evaporator_temperature_profile.png`
- `figures/heat_exchanger_parametric.png`

## Fire-Tube Boiler Notebook

The boiler model is available at
`labs/lab_3/modelo_caldera_lab3.ipynb`. Run the notebook from its own directory
so that it resolves `parametros_nominales_caldera.json`.

The JSON file contains editable nominal values. Replace them with measured
geometry and operating conditions before treating outputs as experimental
validation.

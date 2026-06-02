from __future__ import annotations

from pathlib import Path

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[2]
NOTEBOOK = ROOT / "notebooks" / "Taller5_HX_CoolProp.ipynb"


def main() -> None:
    nb = nbf.v4.new_notebook()
    nb["metadata"]["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    nb["metadata"]["language_info"] = {
        "name": "python",
        "version": "3.9",
    }

    cells = []

    cells.append(
        nbf.v4.new_markdown_cell(
            """# Taller 5 - Termofluidos III

Resolución computacional de los puntos 2 y 3 usando `Python + CoolProp`.

## Nota importante sobre el punto 2

El enunciado no fija completamente el ciclo ideal del `R134a`, por lo que este cuaderno deja **editables** las temperaturas de evaporación y condensación.

El caso base usado en la entrega es:

- `T_evap = 0 °C`
- `T_cond = 40 °C`

Si el profesor da otra pareja de temperaturas, basta cambiar esos dos parámetros y volver a ejecutar el cuaderno.
"""
        )
    )

    cells.append(
        nbf.v4.new_code_cell(
            """from pathlib import Path
import sys

ROOT = Path.cwd().resolve()
MODEL_DIR = ROOT / 'talleres' / 'taller_5'
if str(MODEL_DIR) not in sys.path:
    sys.path.insert(0, str(MODEL_DIR))

import numpy as np
from IPython.display import Image, display
from taller5_hx_model import (
    problem1,
    problem2,
    problem3_design,
    problem3_parametric,
    generate_problem2_figure,
    generate_problem3_figure,
    to_dict,
)
"""
        )
    )

    cells.append(
        nbf.v4.new_markdown_cell(
            """## Punto 1

Aunque el enunciado sugiere `EES` para el factor de corrección `F`, el mismo resultado se puede verificar aquí con la formulación general de Fakheri. El archivo `.ees` entregado reproduce estas ecuaciones.
"""
        )
    )

    cells.append(
        nbf.v4.new_code_cell(
            """p1 = problem1()
to_dict(p1)
"""
        )
    )

    cells.append(
        nbf.v4.new_markdown_cell(
            """## Punto 2

Evaporador de `R134a` modelado como intercambiador tubo-coraza con refrigerante evaporando a temperatura aproximadamente constante.
"""
        )
    )

    cells.append(
        nbf.v4.new_code_cell(
            """T_evap_C = 0.0
T_cond_C = 40.0

p2 = problem2(T_evap_C=T_evap_C, T_cond_C=T_cond_C)
to_dict(p2)
"""
        )
    )

    cells.append(
        nbf.v4.new_code_cell(
            """fig_dir = ROOT / 'outputs'
fig_dir.mkdir(exist_ok=True)
fig_p2 = generate_problem2_figure(p2, fig_dir / 'taller5_p2_temperaturas.png')
display(Image(filename=str(fig_p2)))
"""
        )
    )

    cells.append(
        nbf.v4.new_markdown_cell(
            """## Punto 3

Diseño del doble tubo en contracorriente imponiendo:

- `T_{c,salida} = 350 K`
- `\Delta p_{fría,max} = 15 kPa`
"""
        )
    )

    cells.append(
        nbf.v4.new_code_cell(
            """p3 = problem3_design()
to_dict(p3)
"""
        )
    )

    cells.append(
        nbf.v4.new_code_cell(
            """m_values = np.linspace(0.002, 0.004, 21)
rows = problem3_parametric(D=p3.D_m, L=p3.L_m, m_values=m_values)
fig_p3 = generate_problem3_figure(rows, ROOT / 'outputs' / 'taller5_p3_parametrico.png')
display(Image(filename=str(fig_p3)))
"""
        )
    )

    cells.append(
        nbf.v4.new_markdown_cell(
            """## Comentarios rápidos

- En el punto 2, al aumentar `T_evap` el `LMTD` disminuye con rapidez, por eso la longitud requerida del tubo crece de forma fuerte.
- En el punto 3, con `D` y `L` fijos, aumentar el flujo másico incrementa `\dot Q`, pero reduce la temperatura de salida de la corriente fría porque crece más rápido la capacidad calorífica que el `UA`.
- La caída de presión del punto 3 aumenta de forma no lineal y supera `15 kPa` cuando `\dot m > 0.0025 kg/s`.
"""
        )
    )

    nb["cells"] = cells
    NOTEBOOK.parent.mkdir(parents=True, exist_ok=True)
    NOTEBOOK.write_text(nbf.writes(nb), encoding="utf-8")


if __name__ == "__main__":
    main()

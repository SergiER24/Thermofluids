# Mathematical Formulation

## Energy Balance

For a steady heat exchanger,

```math
\dot Q = \dot m_h c_{p,h}(T_{h,i}-T_{h,o})
= \dot m_c c_{p,c}(T_{c,o}-T_{c,i}).
```

## LMTD Method

```math
\dot Q = UA\Delta T_{lm}
```

```math
\Delta T_{lm} =
\frac{\Delta T_1-\Delta T_2}
{\ln(\Delta T_1/\Delta T_2)}.
```

For shell-and-tube arrangements, a correction factor `F` is applied:

```math
\dot Q = UAF\Delta T_{lm}.
```

## Internal Convection

The reusable model evaluates

```math
Re=\frac{\rho VD}{\mu}, \qquad
Pr=\frac{c_p\mu}{k_f}
```

and uses laminar or turbulent tube-flow correlations to determine `Nu`, then

```math
h=\frac{Nu\,k_f}{D}.
```

## Pressure Loss

The cold-side design constraint is evaluated with

```math
\Delta p = f\frac{L}{D}\frac{\rho V^2}{2}.
```

The double-pipe design solves diameter and length so that heat duty and maximum
pressure drop are satisfied simultaneously.

## Boiler Laboratory Model

The notebook under `labs/lab_3/` extends this methodology to a fire-tube boiler
using:

- methane-equivalent combustion stoichiometry;
- adiabatic flame-temperature solution;
- radiation linearization;
- gas-side convection;
- water-side natural convection;
- wall conduction;
- overall conductance and thermal balances.

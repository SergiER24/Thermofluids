# Computational Thermofluids

This GitHub Pages-ready site documents heat-exchanger sizing, parametric
analysis, and fire-tube boiler modeling completed at Universidad de los Andes.

## Engineering Workflow

```mermaid
flowchart LR
    A[Design inputs] --> B[Energy balances]
    B --> C[CoolProp fluid properties]
    C --> D[Reynolds, Prandtl, Nusselt]
    D --> E[Overall heat-transfer coefficient]
    E --> F[Area and tube-length sizing]
    F --> G[Pressure-drop constraint]
    G --> H[Parametric sensitivity sweep]
    H --> I[Figures and machine-readable results]
```

## Documentation Map

- [Mathematical formulation](mathematical-formulation.md)
- [Reproducibility guide](reproducibility.md)
- [Portfolio evaluation](portfolio-evaluation.md)

## Generated Evidence

![Parametric analysis](assets/heat_exchanger_parametric.png)

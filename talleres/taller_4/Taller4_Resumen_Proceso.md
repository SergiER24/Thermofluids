# Resumen del proceso - Taller 4 de radiacion

## 1. Objetivo

Resolver la transferencia de calor por celda en un panel tipo honeycomb, incluyendo:

- conduccion en las placas externa e interna,
- conduccion en las paredes del honeycomb,
- conveccion natural del aire atrapado,
- radiacion entre las dos caras internas enfrentadas,
- analisis de sensibilidad,
- y un modelo de prediccion para el bono.

## 2. Criterio final adoptado

Despues de revisar el enunciado, las diapositivas de clase y el desarrollo compartido por el companero, el modelo final se dejo asi:

- placas en serie,
- nucleo honeycomb en paralelo,
- radiacion directa entre las dos caras internas de la cavidad usando un factor de vision finito F12,
- conveccion natural en el recinto horizontal calentado por abajo,
- propiedades del aire evaluadas a temperatura de pelicula.

## 3. Datos base del problema

- Tsi = 25 C
- Tso = -10 C
- epsilon = 0.85
- W = 0.01 m
- t = 0.002 m
- L1 = 0.0125 m
- L2 = 0.05 m
- L3 = 0.0125 m
- k1 = 0.0778 W/mK
- k2 = 0.170 W/mK
- aire a 1 atm

La apertura interna de la celda es:

```text
a = W - t
a = 0.01 - 0.002 = 0.008 m
```

## 4. Significado de las variables

- epsilon: emisividad de las superficies internas del tablero. Es una propiedad radiativa entre 0 y 1 que mide que tan eficientemente una superficie emite radiacion termica comparada con una superficie negra.
- W: ancho total de la celda cuadrada.
- t: espesor total de la pared de la celda.
- L1: espesor de la placa interior.
- L2: altura del espacio honeycomb.
- L3: espesor de la placa exterior.
- k1: conductividad termica del tablero de baja densidad.
- k2: conductividad termica del tablero de alta densidad en las paredes del honeycomb.
- Tsi: temperatura de la superficie interior del panel.
- Tso: temperatura de la superficie exterior del panel.
- T0: temperatura de la cara interna inferior de la cavidad.
- T1: temperatura de la cara interna superior de la cavidad.
- Tf: temperatura de pelicula del aire, usada para propiedades.
- F12: factor de vision entre las dos caras internas enfrentadas.
- q: tasa de transferencia de calor por celda.
- q'': flujo de calor por unidad de area total de la celda.
- Ra: numero de Rayleigh de la cavidad.
- Nu: numero de Nusselt de la cavidad.
- hconv: coeficiente convectivo equivalente.

## 5. Geometria y areas

Area total por celda:

```text
Atotal = W^2
```

Area abierta de la cavidad:

```text
Aopen = (W - t)^2
```

Area solida conductiva de las paredes:

```text
Awall = W^2 - (W - t)^2
Awall = 2*W*t - t^2
```

## 6. Resistencias termicas

### 6.1 Conduccion en las placas

```text
Rin = L1 / (k1 * Atotal)
Rout = L3 / (k1 * Atotal)
```

### 6.2 Conduccion por las paredes del honeycomb

```text
Rwall = L2 / (k2 * Awall)
```

### 6.3 Temperatura de pelicula y propiedades del aire

```text
Tf = (T0 + T1) / 2
beta = 1 / Tf
```

Con Tf se calculan:

- densidad rho
- viscosidad dinamica mu
- conductividad termica k_air
- calor especifico cp
- viscosidad cinematica nu
- difusividad termica alpha
- numero de Prandtl Pr

## 7. Conveccion natural en la cavidad

Numero de Rayleigh:

```text
Ra = g * beta * (T0 - T1) * L2^3 / (nu * alpha)
```

Correlacion usada:

```text
Nu = max(1, 0.069 * Ra^(1/3))
```

Coeficiente convectivo:

```text
hconv = Nu * k_air / L2
```

Resistencia convectiva:

```text
Rconv = 1 / (hconv * Aopen)
```

## 8. Radiacion entre las caras internas

Variables adimensionales:

```text
Xbar = (W - t) / L2
Ybar = (W - t) / L2
```

Factor de vision entre rectangulos paralelos finitos:

```text
F12 = (2 / (pi * Xbar * Ybar)) * [
0.5 * ln( ((1 + Xbar^2) * (1 + Ybar^2)) / (1 + Xbar^2 + Ybar^2) )
+ Xbar * sqrt(1 + Ybar^2) * atan( Xbar / sqrt(1 + Ybar^2) )
+ Ybar * sqrt(1 + Xbar^2) * atan( Ybar / sqrt(1 + Xbar^2) )
- Xbar * atan(Xbar)
- Ybar * atan(Ybar)
]
```

Transferencia radiativa entre dos superficies grises difusas:

```text
Qrad = sigma * (T0^4 - T1^4) /
[(1 - epsilon)/(Aopen * epsilon) + 1/(Aopen * F12) + (1 - epsilon)/(Aopen * epsilon)]
```

Resistencia radiativa efectiva:

```text
Rrad,eff = (T0 - T1) / Qrad
```

## 9. Resistencia equivalente del nucleo

Las tres ramas del nucleo quedan en paralelo:

```text
1 / Rcore = 1 / Rwall + 1 / Rconv + 1 / Rrad,eff
```

## 10. Balance total

```text
Rtot = Rin + Rcore + Rout
q = (Tsi - Tso) / Rtot
```

Actualizacion de temperaturas internas:

```text
T0 = Tsi - q * Rin
T1 = Tso + q * Rout
```

## 11. Algoritmo paso a paso

1. Fijar Tsi, Tso, geometria, materiales y epsilon.
2. Calcular Atotal, Aopen y Awall.
3. Calcular Rin, Rout y Rwall.
4. Suponer T0 y T1 iniciales.
5. Calcular Tf.
6. Obtener propiedades del aire con Tf.
7. Calcular Ra, Nu, hconv y Rconv.
8. Calcular F12.
9. Calcular Qrad y Rrad,eff.
10. Calcular Rcore.
11. Calcular q.
12. Actualizar T0 y T1.
13. Repetir hasta convergencia.

## 12. Resultado nominal final

Con el modelo regenerado:

- q = 5.078e-3 W por celda
- q'' = 50.78 W/m2
- T0 = 16.84 C
- T1 = -1.84 C
- Tf = 7.50 C
- F12 = 0.008013
- Ra = 2.964e5
- Nu = 4.601
- hconv = 2.294 W/m2K
- hrad,eff = 0.0401 W/m2K

## 13. Analisis de sensibilidad

Se evaluaron 4 parametros:

- Tso
- Tsi
- L2
- epsilon

Orden de sensibilidad obtenido:

1. Tso
2. Tsi
3. L2
4. epsilon

Conclusion: en esta interpretacion del modelo, epsilon afecta poco porque la rama radiativa es mucho mas resistiva que la convectiva y la conductiva.

## 14. Dataset del bono

La tabla paramatrica de EES no debe iterar T0, T1 o Tf como entradas. Esas son variables internas de solucion.

Las variables elegidas para el dataset fueron las 3 mas sensibles:

- Tso_C
- Tsi_C
- L2_m

Salida principal:

- q_W

Salidas auxiliares recomendadas:

- qpp_W_m2
- T0_C
- T1_C
- Tf_C
- Ra
- Nu
- h_conv_W_m2K
- h_rad_eff_W_m2K
- F12

## 15. Modelo de prediccion usado

Se uso un problema de regresion, no de clasificacion.

Modelos comparados:

- LinearRegression
- PolynomialFeatures degree 2 + LinearRegression
- RandomForestRegressor
- GradientBoostingRegressor

Mejor modelo:

- PolynomialDegree2
- R2 = 0.999890
- RMSE = 1.5e-5 W
- MAE = 1.2e-5 W

## 16. Grafico de dispersion del dataset

El notebook final ya incluye:

- dispersion de q contra cada variable seleccionada,
- y grafico q_real vs q_predicha del mejor modelo.

Cuando exista el CSV exportado desde EES en:

```text
archive/ees_exports/Taller4_Radiacion_dataset.csv
```

el notebook lo lee automaticamente y reemplaza el dataset preliminar.

## 17. Conclusiones cortas

- El modelo fisico primero se corrigio y luego se uso para generar el bono.
- La variable interna de iteracion es Tf, junto con T0 y T1.
- Las variables del dataset son entradas independientes, no variables internas.
- El bono quedo planteado como una regresion multivariable basada en sensibilidad.

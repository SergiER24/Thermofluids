# Revision tecnica de `Taller4-Rad 3.pdf`

> Nota: este archivo conserva la auditoria del desarrollo original.
> El criterio final regenerado quedo sincronizado con el notebook y con el archivo EES.

## Referencias revisadas
- Enunciado base: [Taller4-Rad (1).pdf](Taller4-Rad%20%281%29.pdf)
- Desarrollo auditado: material externo no versionado.

## Correcto
- Se identifico la estructura general del problema como una resistencia en serie formada por placa interior, nucleo honeycomb y placa exterior.
- Se reconocio que dentro del nucleo existen tres mecanismos en paralelo: conduccion por las paredes, conveccion natural en el aire y radiacion.
- La resistencia de conduccion de las placas exterior e interior se planteo con el area total de la celda, \(A = W^2\), lo cual es coherente con la transferencia unidimensional por celda.
- El area solida de las paredes del honeycomb se planteo como
  \[
  A_{\text{wall}} = W^2 - (W-t)^2 = 2Wt - t^2,
  \]
  que es la expresion correcta para la seccion resistente de la rama solida.
- Se detecto correctamente que el problema no cierra con una sola suposicion de temperaturas internas y que hace falta iterar.

## Corregir
- **Unidades del material.** En varias partes aparecen \(k_1\) y \(k_2\) con unidades tipo `W/m^2 K`. Debe ser `W/m K`.
- **Area de la celda.** En la hoja de datos se anota algo cercano a `0.01 m2`; la celda nominal tiene
  \[
  A = W^2 = (0.01)^2 = 1.0\times 10^{-4}\ \text{m}^2.
  \]
- **Geometria interna.** La figura del enunciado muestra \(t/2=1\ \text{mm}\) por lado, por lo que la apertura interna es \(W-t = 8\ \text{mm}\). Esa convencion debe mantenerse en todas las areas y factores de vision.
- **Conveccion natural.** El PDF calcula \(Nu\) sin dejar clara la correlacion, la geometria asociada ni el rango de validez. En el entregable final debe explicitarse la correlacion usada para un recinto horizontal calentado por abajo y enfriado por arriba.
- **Temperaturas asumidas.** En el desarrollo aparecen temperaturas intermedias asumidas y luego se usan en propiedades sin una iteracion consistente. Eso hace que \(Ra\), \(Nu\), \(h\) y las resistencias dependan de un estado que no corresponde al flujo final.
- **Formula radiativa.** Este es el error mas importante. El PDF mezcla dos modelos distintos:
  - usa la expresion de factor de vision para dos rectangulos paralelos separados una distancia \(L_2\)
  - pero al sustituir en la resistencia radiativa termina con una forma equivalente a usar \(F_{12}\approx 1\)
- **Uso inconsistente de \(F_{12}\).** Para la geometria nominal, la formula grafica/analitica de las diapositivas da un valor aproximado
  \[
  F_{12}\approx 0.008.
  \]
  Ese valor por si solo no permite cerrar la radiacion como si el recinto tuviera solo dos superficies. Segun las reglas vistas en clase, la suma de factores para la superficie inferior debe completarse con las paredes laterales internas:
  \[
  F_{12}+F_{13}=1,
  \]
  donde la superficie 3 representa el conjunto de paredes internas agregadas. Asi, para el caso nominal:
  \[
  F_{13}\approx 0.992.
  \]
  El PDF usa la formula de rectangulos paralelos, pero luego no desarrolla de forma consistente el resto del encerramiento. Por eso la resistencia radiativa del documento no es confiable.
- **Chequeo manual final.** El chequeo de temperaturas de la ultima parte del PDF confirma que las temperaturas asumidas no eran correctas. La conclusion correcta no es solo "iterar en EES", sino rearmar el modelo y resolverlo con las ecuaciones no lineales consistentes.
- **Tendencia del bono.** El PDF dice que al aumentar \(\varepsilon\) disminuye la resistencia radiativa, lo cual si es cierto, pero el analisis se queda solo en esa observacion cualitativa. No cuantifica el efecto sobre \(q\), no compara mecanismos y no demuestra sensibilidad sistematica.

## Faltante
- Falta un esquema limpio y legible de la red de resistencias. En el PDF actual se entiende la idea, pero no queda presentado de manera entregable.
- Faltan todas las ecuaciones ordenadas y numeradas para cada rama de la red.
- Falta un algoritmo claro por pasos. El PDF menciona la necesidad de iterar, pero no deja un procedimiento completo reproducible.
- Falta el codigo EES visible. El documento dice que se uso EES, pero el bloque de ecuaciones no aparece de forma que se pueda revisar o reutilizar.
- Falta el bono del enunciado actual en `archive`, que exige al menos 3 parametros y no solo uno.
- Falta el modelo de machine learning: no hay dataset, no hay separacion train/test, no hay metricas \(R^2\), RMSE, MAE, ni comparacion contra resultados fisicos.
- Falta responder la pregunta final del bono sobre la utilidad de modelos de ML frente al calculo de ingenieria tradicional.

## Observacion de fondo sobre la radiacion
Tomando como fuente unicamente las diapositivas del curso, el criterio mas defendible no es el de 2 superficies con \(F_{12}=1\), porque la propia geometria del taller incluye superficies laterales internas que forman parte del encerramiento.

Las diapositivas permiten construir un modelo mas consistente con tres ideas que si aparecen explicitamente en clase:
- la **regla de la suma** del factor de vision,
- la **regla de superposicion**,
- y el **encerramiento de 3 superficies** con superficies reradiantes.

Por eso, en los archivos corregidos se adopta este criterio:
- superficie 1: cara interna inferior,
- superficie 2: cara interna superior,
- superficie 3: conjunto de paredes laterales internas, agregadas como una sola superficie.

Con esa interpretacion:
- \(F_{12}\) se calcula con la formula de dos rectangulos paralelos finitos,
- \(F_{13}=1-F_{12}\),
- \(F_{23}=1-F_{21}\),
- \(F_{31}\) y \(F_{32}\) se obtienen por reciprocidad,
- y \(F_{33}\) se obtiene por la regla de la suma.

Para que el modelo siga siendo manejable con las herramientas vistas en clase, la superficie 3 se aproxima como **reradiante** dentro del submodelo radiativo. Al mismo tiempo, la conduccion axial por las paredes del honeycomb se sigue representando en una rama solida aparte. Esa combinacion es la aproximacion mas cercana a tus diapositivas sin introducir teoria externa.

## Valores guia del modelo corregido
Con el modelo reconstruido y consistente, para el caso nominal del enunciado:

- \(q \approx 6.226\times 10^{-3}\ \text{W}\) por celda
- \(q'' \approx 62.26\ \text{W/m}^2\)
- \(T_1 \approx 15.00\ ^\circ\text{C}\) en la cara interna inferior de la cavidad
- \(T_2 \approx 0.004\ ^\circ\text{C}\) en la cara interna superior de la cavidad
- \(Ra \approx 2.38\times 10^5\)
- \(Nu \approx 4.87\)
- \(F_{12} \approx 0.0080\)
- \(F_{13} = 1 - F_{12} \approx 0.9920\)
- \(F_{31} \approx 0.03968\)
- \(F_{33} \approx 0.92064\)

Estos valores se usaron como referencia para el notebook y para el archivo EES nuevo.

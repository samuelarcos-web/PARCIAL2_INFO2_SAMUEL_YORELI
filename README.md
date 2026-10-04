# PARCIAL2_INFO2_SAMUEL_YORELI

# Parcial 2 - Informática II

## Sistema de procesamiento EEG / ERP


El sistema permite cargar, procesar y visualizar información proveniente de archivos CSV y MAT correspondientes a registros de electroencefalografía (EEG) y potenciales relacionados con eventos (ERP).

---

## Integrantes

- Samuel Arcos
- Yoreli Fuelpaz

---

## Estructura del proyecto

El proyecto está dividido principalmente en dos archivos Python:

### `clases.py`

Contiene:

- Funciones de validación.
- Funciones de suma, resta y multiplicación.
- Clase `ArchivoCSV`.
- Clase `ArchivoMAT`.
- Clase `GestorArchivos`.

### `archivos.py`

Contiene:

- Menú principal.
- Selección de archivos.
- Interacción con el usuario.
- Uso de los objetos CSV y MAT.
- Gestión de los objetos creados.

---

# Funcionalidades CSV

La clase `ArchivoCSV` permite:

- Cargar archivos `.csv`.
- Convertir la columna `time_ms` en índice.
- Mostrar información mediante `info()`.
- Mostrar estadísticas mediante `describe()`.
- Mostrar los canales EEG disponibles.
- Seleccionar una condición.
- Generar un gráfico Stem.
- Resaltar el instante `t = 0 ms`.
- Generar un histograma.
- Generar un gráfico Scatter.
- Mostrar los tres gráficos simultáneamente mediante subplots.
- Guardar automáticamente los gráficos generados.
- Calcular la diferencia entre dos canales seleccionados.

Los canales disponibles en los archivos utilizados incluyen:

- Fz
- FCz
- Cz
- FC3
- FC4
- C3
- C4
- CP3
- CP4

---

# Funcionalidades MAT

La clase `ArchivoMAT` permite:

- Cargar archivos `.mat`.
- Consultar sus variables mediante `whosmat`.
- Mostrar:
  - Nombre de la variable.
  - Dimensiones.
  - Tipo de dato.
- Mantener la matriz tridimensional original.
- Seleccionar una época para obtener una representación 2D.
- Seleccionar cuatro canales.
- Seleccionar un intervalo de muestras.
- Aplicar:
  - Suma.
  - Resta.
  - Multiplicación.
- Graficar los cuatro canales seleccionados.
- Graficar el resultado de la operación.
- Trabajar con una frecuencia de muestreo de 250 Hz.
- Mostrar el tiempo en segundos.
- Calcular promedio y desviación estándar sobre dos ejes seleccionados.
- Mostrar la forma de los vectores resultantes.
- Generar boxplots del promedio y desviación estándar.

---

# Gestor de objetos

También se implementó una clase adicional llamada `GestorArchivos`.

Esta permite:

- Almacenar los objetos CSV y MAT creados.
- Listar los objetos almacenados.
- Buscar objetos por nombre.
- Activar nuevamente un objeto previamente cargado.

---

# Archivos utilizados

## CSV

- `ERP_01.csv`
- `ERP_02.csv`
- `ERP_03.csv`

## MAT

- `Sensitive_Cue.mat`
- `Sound_Cue.mat`
- `Visual_Cue.mat`

---

# Librerías utilizadas

El proyecto utiliza:

```text
pandas
numpy
matplotlib
scipy
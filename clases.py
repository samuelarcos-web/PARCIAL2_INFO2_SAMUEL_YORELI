import os
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
import numpy as np
from scipy.io import loadmat, whosmat



def suma(a, b, c, d):
    return a + b + c + d


def resta(a, b, c, d):
    return a - b - c - d


def multiplicacion(a, b, c, d):
    return a * b * c * d

def validar_canal_lista(mensaje, canales_disponibles):
    while True:
        canal = input(mensaje).strip()

        if canal in canales_disponibles:
            return canal

        print(
            "Canal inválido. Canales disponibles:",
            ", ".join(canales_disponibles)
        )

def validar_diferentes(valor1, valor2, mensaje):
    if valor1 == valor2:
        raise ValueError(mensaje)

def validar_entero(mensaje, minimo=None, maximo=None):
    while True:
        try:
            valor = int(input(mensaje))

            if minimo is not None and valor < minimo:
                print(f"El valor debe ser mayor o igual a {minimo}.")
                continue

            if maximo is not None and valor > maximo:
                print(f"El valor debe ser menor o igual a {maximo}.")
                continue

            return valor

        except ValueError:
            print("Entrada inválida. Debe ingresar un número entero.")


def validar_opcion(mensaje, opciones_validas):
    while True:
        opcion = input(mensaje).strip()

        if opcion in opciones_validas:
            return opcion

        print(
            "Opción inválida. Opciones permitidas:",
            ", ".join(opciones_validas)
        )


def validar_canal(nombre_canal, canales_disponibles):
    if nombre_canal not in canales_disponibles:
        raise ValueError(
            f"El canal '{nombre_canal}' no existe."
        )

    return nombre_canal

class ArchivoCSV:

    def __init__(self, ruta):
        self.ruta = ruta
        self.datos = pd.read_csv(ruta)

        if "time_ms" in self.datos.columns:
            self.datos.set_index("time_ms", inplace=True)

    def __str__(self):
        buffer = StringIO()

        self.datos.info(buf=buffer)

        informacion = buffer.getvalue()

        descripcion = self.datos.describe().to_string()

        return (
            "INFORMACIÓN DEL ARCHIVO CSV\n\n"
            + informacion
            + "\nDESCRIPCIÓN ESTADÍSTICA\n\n"
            + descripcion
        )

    def mostrar_canales(self):
        columnas_no_canales = ["subject", "condition"]

        canales = [
            columna
            for columna in self.datos.columns
            if columna not in columnas_no_canales
        ]

        return canales

    def graficar_condicion(self, condicion, canal_stem, canal_hist, canal_x, canal_y):

        datos_condicion = self.datos[
            self.datos["condition"] == condicion
        ]

        fig = plt.figure(figsize=(12, 8))

        ax1 = plt.subplot(2, 2, (1, 2))
        ax2 = plt.subplot(2, 2, 3)
        ax3 = plt.subplot(2, 2, 4)

        # STEM
        ax1.stem(
            datos_condicion.index,
            datos_condicion[canal_stem]
        )

        ax1.axvline(
            x=0,
            linestyle="--"
        )

        ax1.set_title(
            f"Stem de {canal_stem} - Condición {condicion}"
        )

        ax1.set_xlabel("Tiempo (ms)")
        ax1.set_ylabel("Amplitud (µV)")

        # HISTOGRAMA
        ax2.hist(
            datos_condicion[canal_hist],
            bins=30
        )

        ax2.set_title(
            f"Histograma de {canal_hist}"
        )

        ax2.set_xlabel("Amplitud (µV)")
        ax2.set_ylabel("Frecuencia")

        # SCATTER
        ax3.scatter(
            datos_condicion[canal_x],
            datos_condicion[canal_y]
        )

        ax3.set_title(
            f"{canal_x} vs {canal_y}"
        )

        ax3.set_xlabel(
            f"{canal_x} (µV)"
        )

        ax3.set_ylabel(
            f"{canal_y} (µV)"
        )

        plt.tight_layout()

        nombre = (
            f"graficos_condicion_{condicion}.png"
        )

        os.makedirs("graficos", exist_ok=True)

        plt.savefig(f"graficos/{nombre}", dpi=300)

        plt.show()

    def diferencia_interhemisferica(self, canal_izquierdo, canal_derecho):

        nombre_columna = (
            f"{canal_izquierdo}_{canal_derecho}"
        )

        self.datos[nombre_columna] = (
            self.datos[canal_izquierdo]
            - self.datos[canal_derecho]
        )

        return self.datos[
            [
                canal_izquierdo,
                canal_derecho,
                nombre_columna
            ]
        ]

class ArchivoMAT:

    def __init__(self, ruta):
        self.ruta = ruta

        # Información de las variables contenidas en el archivo MAT
        self.variables = whosmat(ruta)

        # Carga completa del archivo
        contenido = loadmat(ruta)

        # Se eliminan las llaves internas creadas por MATLAB
        llaves = [
            llave for llave in contenido.keys()
            if not llave.startswith("__")
        ]

        if len(llaves) == 0:
            raise ValueError("El archivo MAT no contiene variables válidas.")

        # Para estos archivos trabajaremos con la primera variable útil
        self.nombre_variable = llaves[0]

        # Matriz original sin modificar
        self.matriz_original = contenido[self.nombre_variable]

        if self.matriz_original.ndim != 3:
            raise ValueError(
                "La matriz principal debe tener tres dimensiones."
            )

        # Frecuencia de muestreo dada por el enunciado
        self.frecuencia_muestreo = 250

    def __str__(self):

        texto = "\nINFORMACIÓN DEL ARCHIVO MAT\n\n"

        texto += f"Archivo: {self.ruta}\n\n"

        texto += (
            f"{'Variable':<20}"
            f"{'Dimensiones':<20}"
            f"{'Tipo'}\n"
        )

        texto += "-" * 60 + "\n"

        for nombre, dimensiones, tipo in self.variables:

            texto += (
                f"{nombre:<20}"
                f"{str(dimensiones):<20}"
                f"{tipo}\n"
            )

        return texto
    def operar_canales(
        self,
        funcion,
        canales,
        punto_min,
        punto_max,
        epoca=0
    ):

        if len(canales) != 4:
            raise ValueError(
                "Debe seleccionar exactamente 4 canales."
            )

        if epoca < 0 or epoca >= self.matriz_original.shape[2]:
            raise ValueError(
                "La época seleccionada está fuera de rango."
            )

        # Convertimos la matriz 3D a una matriz 2D
        # tomando una época específica
        matriz_2d = self.matriz_original[:, :, epoca]

        if punto_min < 0 or punto_max > matriz_2d.shape[1]:
            raise ValueError(
                "El rango de muestras está fuera de los límites."
            )

        if punto_min >= punto_max:
            raise ValueError(
                "El punto mínimo debe ser menor al punto máximo."
            )

        for canal in canales:
            if canal < 0 or canal >= matriz_2d.shape[0]:
                raise ValueError(
                    f"El canal {canal} está fuera de rango."
                )

        # Selección del intervalo solicitado
        datos = matriz_2d[
            canales,
            punto_min:punto_max
        ]

        # Aplicamos la función recibida
        resultado = funcion(
            datos[0],
            datos[1],
            datos[2],
            datos[3]
        )

        # Conversión de muestras a segundos
        tiempo = (
            np.arange(punto_min, punto_max)
            / self.frecuencia_muestreo
        )

        fig, (ax1, ax2) = plt.subplots(
            2,
            1,
            figsize=(12, 8)
        )

        # Primer subplot: cuatro canales
        for i, canal in enumerate(canales):
            ax1.plot(
                tiempo,
                datos[i],
                label=f"Canal {canal}"
            )

        ax1.set_title(
            f"Canales seleccionados - Época {epoca}"
        )
        ax1.set_xlabel("Tiempo (s)")
        ax1.set_ylabel("Amplitud (µV)")
        ax1.legend()
        ax1.grid(True)

        # Nombre de la operación
        nombre_operacion = funcion.__name__

        # Segundo subplot: resultado
        ax2.plot(
            tiempo,
            resultado,
            label=nombre_operacion
        )

        ax2.set_title(
            f"Resultado de la operación: {nombre_operacion}"
        )
        ax2.set_xlabel("Tiempo (s)")
        ax2.set_ylabel("Amplitud (µV)")
        ax2.legend()
        ax2.grid(True)

        plt.tight_layout()

        nombre_archivo = (
            f"graficos/"
            f"MAT_{nombre_operacion}_epoca_{epoca}.png"
        )

        os.makedirs("graficos", exist_ok=True)

        plt.savefig(
            nombre_archivo,
            dpi=300
        )

        plt.show()

        return resultado

    def estadisticas_3d(self, eje1, eje2):

        # Validación de los ejes
        ejes_validos = [0, 1, 2]

        if eje1 not in ejes_validos or eje2 not in ejes_validos:
            raise ValueError(
                "Los ejes deben ser 0, 1 o 2."
            )

        if eje1 == eje2:
            raise ValueError(
                "Debe seleccionar dos ejes diferentes."
            )

        # Cálculo sobre la matriz 3D ORIGINAL
        promedio = np.mean(
            self.matriz_original,
            axis=(eje1, eje2)
        )

        desviacion = np.std(
            self.matriz_original,
            axis=(eje1, eje2)
        )

        # Mostrar las formas resultantes
        print(
            "\nForma del vector de promedio:",
            promedio.shape
        )

        print(
            "Forma del vector de desviación estándar:",
            desviacion.shape
        )

        # Boxplots
        fig, ax = plt.subplots(
            figsize=(9, 6)
        )

        ax.boxplot(
            [promedio, desviacion],
            labels=[
                "Promedio",
                "Desviación estándar"
            ]
        )

        ax.set_title(
            f"Distribución estadística - Ejes {eje1} y {eje2}"
        )

        ax.set_ylabel("Amplitud (µV)")

        ax.grid(True)

        plt.tight_layout()

        nombre_archivo = (
            f"graficos/"
            f"MAT_estadisticas_ejes_{eje1}_{eje2}.png"
        )

        os.makedirs("graficos", exist_ok=True)

        plt.savefig(
            nombre_archivo,
            dpi=300
        )

        plt.show()

        return promedio, desviacion
    
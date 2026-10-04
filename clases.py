import os
from io import StringIO

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.io import loadmat, whosmat


# =========================================================
# FUNCIONES DE VALIDACIÓN
# =========================================================

def validar_entero(mensaje, minimo=None, maximo=None):

    while True:

        try:
            valor = int(input(mensaje))

            if minimo is not None and valor < minimo:
                print(
                    f"El valor debe ser mayor o igual a {minimo}."
                )
                continue

            if maximo is not None and valor > maximo:
                print(
                    f"El valor debe ser menor o igual a {maximo}."
                )
                continue

            return valor

        except ValueError:
            print(
                "Entrada inválida. "
                "Debe ingresar un número entero."
            )


def validar_opcion(mensaje, opciones_validas):

    while True:

        opcion = input(mensaje).strip()

        if opcion in opciones_validas:
            return opcion

        print(
            "Opción inválida. Opciones permitidas:",
            ", ".join(opciones_validas)
        )


def validar_canal_lista(
    mensaje,
    canales_disponibles
):

    while True:

        canal = input(mensaje).strip()

        if canal in canales_disponibles:
            return canal

        print(
            "Canal inválido. Canales disponibles:",
            ", ".join(canales_disponibles)
        )


# =========================================================
# FUNCIONES PARA OPERACIONES MAT
# =========================================================

def suma(a, b, c, d):
    return a + b + c + d


def resta(a, b, c, d):
    return a - b - c - d


def multiplicacion(a, b, c, d):
    return a * b * c * d


# =========================================================
# GESTOR DE OBJETOS
# =========================================================

class GestorArchivos:

    def __init__(self):
        self.objetos = {}

    def agregar(
        self,
        nombre,
        objeto
    ):
        self.objetos[nombre] = objeto

    def buscar(
        self,
        nombre
    ):

        if nombre in self.objetos:
            return self.objetos[nombre]

        return None

    def listar(self):
        return list(
            self.objetos.keys()
        )

    def __str__(self):

        if not self.objetos:
            return "No hay objetos almacenados."

        texto = "OBJETOS ALMACENADOS\n"
        texto += "-" * 30 + "\n"

        for nombre, objeto in self.objetos.items():

            texto += (
                f"{nombre} -> "
                f"{type(objeto).__name__}\n"
            )

        return texto


# =========================================================
# CLASE PARA ARCHIVOS CSV
# =========================================================

class ArchivoCSV:

    def __init__(
        self,
        ruta
    ):

        self.ruta = ruta

        # Validar extensión
        if not ruta.lower().endswith(".csv"):

            raise ValueError(
                "El archivo seleccionado "
                "debe tener extensión .csv"
            )

        self.datos = pd.read_csv(
            ruta
        )

        # Convertir el tiempo en índice
        if "time_ms" in self.datos.columns:

            self.datos.set_index(
                "time_ms",
                inplace=True
            )


    # -----------------------------------------------------
    # INFORMACIÓN DEL ARCHIVO
    # -----------------------------------------------------

    def __str__(self):

        buffer = StringIO()

        self.datos.info(
            buf=buffer
        )

        informacion = buffer.getvalue()

        descripcion = (
            self.datos
            .describe()
            .to_string()
        )

        return (
            "INFORMACIÓN DEL ARCHIVO CSV\n\n"
            + informacion
            + "\nDESCRIPCIÓN ESTADÍSTICA\n\n"
            + descripcion
        )


    # -----------------------------------------------------
    # MOSTRAR CANALES
    # -----------------------------------------------------

    def mostrar_canales(self):

        columnas_no_canales = [
            "subject",
            "condition"
        ]

        canales = [
            columna
            for columna in self.datos.columns
            if columna not in columnas_no_canales
        ]

        return canales


    # -----------------------------------------------------
    # GRÁFICOS SEGÚN CONDICIÓN
    # -----------------------------------------------------

    def graficar_condicion(
        self,
        condicion,
        canal_stem,
        canal_hist,
        canal_x,
        canal_y
    ):

        datos_condicion = self.datos[
            self.datos["condition"]
            == condicion
        ]

        if datos_condicion.empty:

            raise ValueError(
                "No existen datos para "
                "la condición seleccionada."
            )

        fig = plt.figure(
            figsize=(12, 8)
        )

        # Stem ocupa toda la parte superior
        ax1 = plt.subplot(
            2,
            2,
            (1, 2)
        )

        # Histograma abajo izquierda
        ax2 = plt.subplot(
            2,
            2,
            3
        )

        # Scatter abajo derecha
        ax3 = plt.subplot(
            2,
            2,
            4
        )


        # ---------------------------------------------
        # STEM
        # ---------------------------------------------

        ax1.stem(
            datos_condicion.index,
            datos_condicion[canal_stem]
        )

        ax1.axvline(
            x=0,
            linestyle="--"
        )

        ax1.set_title(
            f"Stem de {canal_stem} "
            f"- Condición {condicion}"
        )

        ax1.set_xlabel(
            "Tiempo (ms)"
        )

        ax1.set_ylabel(
            "Amplitud (µV)"
        )


        # ---------------------------------------------
        # HISTOGRAMA
        # ---------------------------------------------

        ax2.hist(
            datos_condicion[canal_hist],
            bins=30
        )

        ax2.set_title(
            f"Histograma de {canal_hist}"
        )

        ax2.set_xlabel(
            "Amplitud (µV)"
        )

        ax2.set_ylabel(
            "Frecuencia"
        )


        # ---------------------------------------------
        # SCATTER
        # ---------------------------------------------

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


        # ---------------------------------------------
        # GUARDAR GRÁFICO
        # ---------------------------------------------

        plt.tight_layout()

        os.makedirs(
            "graficos",
            exist_ok=True
        )

        nombre_base = os.path.splitext(
            os.path.basename(
                self.ruta
            )
        )[0]

        nombre = (
            f"{nombre_base}_"
            f"condicion_{condicion}.png"
        )

        plt.savefig(
            f"graficos/{nombre}",
            dpi=300
        )

        plt.show()


    # -----------------------------------------------------
    # DIFERENCIA INTERHEMISFÉRICA
    # -----------------------------------------------------

    def diferencia_interhemisferica(
        self,
        canal_izquierdo,
        canal_derecho
    ):

        if canal_izquierdo not in self.datos.columns:

            raise ValueError(
                f"El canal {canal_izquierdo} "
                "no existe."
            )

        if canal_derecho not in self.datos.columns:

            raise ValueError(
                f"El canal {canal_derecho} "
                "no existe."
            )

        if canal_izquierdo == canal_derecho:

            raise ValueError(
                "Los canales deben ser diferentes."
            )

        nombre_columna = (
            f"{canal_izquierdo}_"
            f"{canal_derecho}"
        )

        self.datos[
            nombre_columna
        ] = (
            self.datos[canal_izquierdo]
            -
            self.datos[canal_derecho]
        )

        return self.datos[
            [
                canal_izquierdo,
                canal_derecho,
                nombre_columna
            ]
        ]


# =========================================================
# CLASE PARA ARCHIVOS MAT
# =========================================================

class ArchivoMAT:

    def __init__(
        self,
        ruta
    ):

        self.ruta = ruta

        # Validar extensión
        if not ruta.lower().endswith(".mat"):

            raise ValueError(
                "El archivo seleccionado "
                "debe tener extensión .mat"
            )

        # Información del archivo mediante whosmat
        self.variables = whosmat(
            ruta
        )

        # Cargar contenido completo
        contenido = loadmat(
            ruta
        )

        # Eliminar llaves internas de MATLAB
        llaves = [
            llave
            for llave in contenido.keys()
            if not llave.startswith("__")
        ]

        if len(llaves) == 0:

            raise ValueError(
                "El archivo MAT no contiene "
                "variables válidas."
            )

        # Primera variable útil
        self.nombre_variable = llaves[0]

        # Matriz 3D original
        self.matriz_original = contenido[
            self.nombre_variable
        ]

        if self.matriz_original.ndim != 3:

            raise ValueError(
                "La matriz principal debe "
                "tener tres dimensiones."
            )

        # Frecuencia dada por el parcial
        self.frecuencia_muestreo = 250


    # -----------------------------------------------------
    # INFORMACIÓN MAT
    # -----------------------------------------------------

    def __str__(self):

        texto = (
            "\nINFORMACIÓN DEL ARCHIVO MAT\n\n"
        )

        texto += (
            f"Archivo: {self.ruta}\n\n"
        )

        texto += (
            f"{'Variable':<20}"
            f"{'Dimensiones':<20}"
            f"{'Tipo'}\n"
        )

        texto += (
            "-" * 60
            + "\n"
        )

        for (
            nombre,
            dimensiones,
            tipo
        ) in self.variables:

            texto += (
                f"{nombre:<20}"
                f"{str(dimensiones):<20}"
                f"{tipo}\n"
            )

        return texto


    # -----------------------------------------------------
    # OPERACIONES CON 4 CANALES
    # -----------------------------------------------------

    def operar_canales(
        self,
        funcion,
        canales,
        punto_min,
        punto_max,
        epoca=0
    ):

        # Deben ser 4 canales
        if len(canales) != 4:

            raise ValueError(
                "Debe seleccionar exactamente "
                "4 canales."
            )

        # Los canales deben ser diferentes
        if len(set(canales)) != 4:

            raise ValueError(
                "Los cuatro canales seleccionados "
                "deben ser diferentes."
            )

        # Validar época
        if (
            epoca < 0
            or epoca
            >= self.matriz_original.shape[2]
        ):

            raise ValueError(
                "La época seleccionada "
                "está fuera de rango."
            )

        # ---------------------------------------------
        # CONVERTIR MATRIZ 3D A 2D
        # ---------------------------------------------

        matriz_2d = self.matriz_original[
            :,
            :,
            epoca
        ]

        # ---------------------------------------------
        # VALIDAR RANGO
        # ---------------------------------------------

        if (
            punto_min < 0
            or punto_max
            > matriz_2d.shape[1]
        ):

            raise ValueError(
                "El rango de muestras está "
                "fuera de los límites."
            )

        if punto_min >= punto_max:

            raise ValueError(
                "El punto mínimo debe ser "
                "menor al punto máximo."
            )

        # ---------------------------------------------
        # VALIDAR CANALES
        # ---------------------------------------------

        for canal in canales:

            if (
                canal < 0
                or canal
                >= matriz_2d.shape[0]
            ):

                raise ValueError(
                    f"El canal {canal} "
                    "está fuera de rango."
                )

        # ---------------------------------------------
        # EXTRAER DATOS
        # ---------------------------------------------

        datos = matriz_2d[
            canales,
            punto_min:punto_max
        ]

        # ---------------------------------------------
        # APLICAR OPERACIÓN
        # ---------------------------------------------

        resultado = funcion(
            datos[0],
            datos[1],
            datos[2],
            datos[3]
        )

        # ---------------------------------------------
        # CONVERSIÓN DE MUESTRAS A SEGUNDOS
        # ---------------------------------------------

        tiempo = (
            np.arange(
                punto_min,
                punto_max
            )
            /
            self.frecuencia_muestreo
        )

        # ---------------------------------------------
        # CREAR SUBPLOTS
        # ---------------------------------------------

        fig, (
            ax1,
            ax2
        ) = plt.subplots(
            2,
            1,
            figsize=(12, 8)
        )

        # ---------------------------------------------
        # PRIMER SUBPLOT:
        # 4 CANALES
        # ---------------------------------------------

        for i, canal in enumerate(
            canales
        ):

            ax1.plot(
                tiempo,
                datos[i],
                label=f"Canal {canal}"
            )

        ax1.set_title(
            f"Canales seleccionados "
            f"- Época {epoca}"
        )

        ax1.set_xlabel(
            "Tiempo (s)"
        )

        ax1.set_ylabel(
            "Amplitud (µV)"
        )

        ax1.legend()

        ax1.grid(
            True
        )

        # ---------------------------------------------
        # SEGUNDO SUBPLOT:
        # RESULTADO DE LA OPERACIÓN
        # ---------------------------------------------

        nombre_operacion = funcion.__name__

        ax2.plot(
            tiempo,
            resultado,
            label=nombre_operacion
        )

        ax2.set_title(
            f"Resultado de la operación: "
            f"{nombre_operacion}"
        )

        ax2.set_xlabel(
            "Tiempo (s)"
        )

        ax2.set_ylabel(
            "Amplitud (µV)"
        )

        ax2.legend()

        ax2.grid(
            True
        )

        # ---------------------------------------------
        # GUARDAR GRÁFICO
        # ---------------------------------------------

        plt.tight_layout()

        os.makedirs(
            "graficos",
            exist_ok=True
        )

        nombre_base = os.path.splitext(
            os.path.basename(
                self.ruta
            )
        )[0]

        nombre_archivo = (
            f"graficos/"
            f"{nombre_base}_"
            f"{nombre_operacion}_"
            f"epoca_{epoca}.png"
        )

        plt.savefig(
            nombre_archivo,
            dpi=300
        )

        plt.show()

        return resultado


    # -----------------------------------------------------
    # ESTADÍSTICAS SOBRE MATRIZ 3D ORIGINAL
    # -----------------------------------------------------

    def estadisticas_3d(
        self,
        eje1,
        eje2
    ):

        ejes_validos = [
            0,
            1,
            2
        ]

        if (
            eje1 not in ejes_validos
            or eje2 not in ejes_validos
        ):

            raise ValueError(
                "Los ejes deben ser 0, 1 o 2."
            )

        if eje1 == eje2:

            raise ValueError(
                "Debe seleccionar "
                "dos ejes diferentes."
            )

        # ---------------------------------------------
        # PROMEDIO
        # ---------------------------------------------

        promedio = np.mean(
            self.matriz_original,
            axis=(
                eje1,
                eje2
            )
        )

        # ---------------------------------------------
        # DESVIACIÓN ESTÁNDAR
        # ---------------------------------------------

        desviacion = np.std(
            self.matriz_original,
            axis=(
                eje1,
                eje2
            )
        )

        # ---------------------------------------------
        # MOSTRAR FORMAS
        # ---------------------------------------------

        print(
            "\nForma del vector de promedio:",
            promedio.shape
        )

        print(
            "Forma del vector de desviación estándar:",
            desviacion.shape
        )

        # ---------------------------------------------
        # BOXPLOTS
        # ---------------------------------------------

        fig, ax = plt.subplots(
            figsize=(9, 6)
        )

        ax.boxplot(
            [
                promedio,
                desviacion
            ],
            labels=[
                "Promedio",
                "Desviación estándar"
            ]
        )

        ax.set_title(
            f"Distribución estadística "
            f"- Ejes {eje1} y {eje2}"
        )

        ax.set_ylabel(
            "Amplitud (µV)"
        )

        ax.grid(
            True
        )

        # ---------------------------------------------
        # GUARDAR GRÁFICO
        # ---------------------------------------------

        plt.tight_layout()

        os.makedirs(
            "graficos",
            exist_ok=True
        )

        nombre_base = os.path.splitext(
            os.path.basename(
                self.ruta
            )
        )[0]

        nombre_archivo = (
            f"graficos/"
            f"{nombre_base}_"
            f"estadisticas_ejes_"
            f"{eje1}_{eje2}.png"
        )

        plt.savefig(
            nombre_archivo,
            dpi=300
        )

        plt.show()

        return (
            promedio,
            desviacion
        )
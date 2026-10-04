import os

from clases import (
    ArchivoCSV,
    ArchivoMAT,
    GestorArchivos,
    suma,
    resta,
    multiplicacion,
    validar_entero,
    validar_opcion,
    validar_canal_lista
)


archivo_csv = None
archivo_mat = None

gestor = GestorArchivos()


def mostrar_menu():
    print("\n" + "=" * 55)
    print("        SISTEMA DE PROCESAMIENTO EEG / ERP")
    print("=" * 55)

    print("\nARCHIVOS CSV")
    print("1. Cargar archivo CSV")
    print("2. Mostrar información del CSV")
    print("3. Mostrar canales disponibles")
    print("4. Graficar condición")
    print("5. Diferencia interhemisférica")

    print("\nARCHIVOS MAT")
    print("6. Cargar archivo MAT")
    print("7. Mostrar información del MAT")
    print("8. Operar cuatro canales")
    print("9. Estadísticas de matriz 3D")

    print("\n0. Salir")

    print("\nEjemplos de rutas:")
    print("CSV: datos/Arch_CSV/ERP_01.csv")
    print("MAT: datos/Archs_MAT/Sensitive_Cue.mat")

    print("\nGESTOR DE OBJETOS")
    print("10. Listar objetos almacenados")
    print("11. Buscar objeto por nombre")

def seleccionar_archivo(carpeta, extension):

    archivos = [
        archivo
        for archivo in os.listdir(carpeta)
        if archivo.lower().endswith(extension.lower())
    ]

    if not archivos:
        print(f"\nNo se encontraron archivos {extension} en {carpeta}.")
        return None

    print("\nArchivos disponibles:")

    for i, archivo in enumerate(archivos, start=1):
        print(f"{i}. {archivo}")

    opcion = validar_entero(
        "Seleccione un archivo: ",
        1,
        len(archivos)
    )

    archivo_seleccionado = archivos[opcion - 1]

    return os.path.join(
        carpeta,
        archivo_seleccionado
    )


while True:

    mostrar_menu()

    opcion = validar_entero(
        "\nSeleccione una opción: ",
        0,
        11
    )

    # ==========================================
    # SALIR
    # ==========================================

    if opcion == 0:
        print("\nPrograma finalizado correctamente.")
        print("Gracias por utilizar el sistema EEG / ERP.")
        break

    # ==========================================
    # CARGAR CSV
    # ==========================================

    elif opcion == 1:

        ruta = seleccionar_archivo(
            "datos/Arch_CSV",
            ".csv"
        )

        if ruta is not None:

            try:
                archivo_csv = ArchivoCSV(ruta)

                nombre = os.path.basename(ruta)
                gestor.agregar(nombre, archivo_csv)

                print(
                    "\nArchivo CSV cargado correctamente."
                )

            except Exception as error:
                print(
                    "\nError al cargar el archivo:",
                    error
                )

    # ==========================================
    # INFORMACIÓN CSV
    # ==========================================

    elif opcion == 2:

        if archivo_csv is None:
            print(
                "\nPrimero debe cargar un archivo CSV."
            )

        else:
            print(archivo_csv)

    # ==========================================
    # MOSTRAR CANALES CSV
    # ==========================================

    elif opcion == 3:

        if archivo_csv is None:
            print(
                "\nPrimero debe cargar un archivo CSV."
            )

        else:
            print("\nCanales disponibles:")

            for canal in archivo_csv.mostrar_canales():
                print("-", canal)

    # ==========================================
    # GRÁFICOS CSV
    # ==========================================

    elif opcion == 4:

        if archivo_csv is None:
            print(
                "\nPrimero debe cargar un archivo CSV."
            )

        else:

            canales = archivo_csv.mostrar_canales()

            print("\nCanales disponibles:")
            print(", ".join(canales))

            condicion = validar_entero(
                "Seleccione la condición (1, 2 o 3): ",
                1,
                3
            )

            canal_stem = validar_canal_lista(
                "Canal para Stem: ",
                canales
            )

            canal_hist = validar_canal_lista(
                "Canal para Histograma: ",
                canales
            )

            canal_x = validar_canal_lista(
                "Canal X para Scatter: ",
                canales
            )

            canal_y = validar_canal_lista(
                "Canal Y para Scatter: ",
                canales
            )

            try:
                archivo_csv.graficar_condicion(
                    condicion,
                    canal_stem,
                    canal_hist,
                    canal_x,
                    canal_y
                )

            except Exception as error:
                print(
                    "\nError al generar los gráficos:",
                    error
                )

    # ==========================================
    # DIFERENCIA INTERHEMISFÉRICA
    # ==========================================

    elif opcion == 5:

        if archivo_csv is None:
            print(
                "\nPrimero debe cargar un archivo CSV."
            )

        else:

            canales = archivo_csv.mostrar_canales()

            print("\nCanales disponibles:")
            print(", ".join(canales))

            canal_izquierdo = validar_canal_lista(
                "Seleccione canal izquierdo: ",
                canales
            )

            canal_derecho = validar_canal_lista(
                "Seleccione canal derecho: ",
                canales
            )

            if canal_izquierdo == canal_derecho:
                print(
                    "\nDebe seleccionar dos canales diferentes."
                )

            else:

                try:
                    resultado = (
                        archivo_csv
                        .diferencia_interhemisferica(
                            canal_izquierdo,
                            canal_derecho
                        )
                    )

                    print("\nResultado:")
                    print(resultado.head())

                except Exception as error:
                    print(
                        "\nError al calcular la diferencia:",
                        error
                    )

    # ==========================================
    # CARGAR MAT
    # ==========================================

    elif opcion == 6:

        ruta = seleccionar_archivo(
            "datos/Archs_MAT",
            ".mat"
        )

        if ruta is not None:

            try:
                archivo_mat = ArchivoMAT(ruta)

                nombre = os.path.basename(ruta)
                gestor.agregar(nombre, archivo_mat)

                print(
                    "\nArchivo MAT cargado correctamente."
                )

            except Exception as error:
                print(
                    "\nError al cargar el archivo:",
                    error
                )

    # ==========================================
    # INFORMACIÓN MAT
    # ==========================================

    elif opcion == 7:

        if archivo_mat is None:
            print(
                "\nPrimero debe cargar un archivo MAT."
            )

        else:
            print(archivo_mat)

    # ==========================================
    # OPERACIONES CON 4 CANALES MAT
    # ==========================================

    elif opcion == 8:

        if archivo_mat is None:
            print(
                "\nPrimero debe cargar un archivo MAT."
            )

        else:

            cantidad_canales = (
                archivo_mat.matriz_original.shape[0]
            )

            cantidad_muestras = (
                archivo_mat.matriz_original.shape[1]
            )

            cantidad_epocas = (
                archivo_mat.matriz_original.shape[2]
            )

            print(
                "\nNúmero de canales disponibles:",
                cantidad_canales
            )

            canales = []

            for i in range(4):

                canal = validar_entero(
                    f"Ingrese canal {i + 1}: ",
                    0,
                    cantidad_canales - 1
                )

                canales.append(canal)

            punto_min = validar_entero(
                "Punto mínimo: ",
                0,
                cantidad_muestras - 1
            )

            punto_max = validar_entero(
                "Punto máximo: ",
                1,
                cantidad_muestras
            )

            if punto_min >= punto_max:

                print(
                    "\nEl punto mínimo debe ser "
                    "menor al punto máximo."
                )

            else:

                epoca = validar_entero(
                    "Seleccione época: ",
                    0,
                    cantidad_epocas - 1
                )

                print("\nOperaciones disponibles:")
                print("1. Suma")
                print("2. Resta")
                print("3. Multiplicación")

                operacion = validar_opcion(
                    "Seleccione operación: ",
                    ["1", "2", "3"]
                )

                funciones = {
                    "1": suma,
                    "2": resta,
                    "3": multiplicacion
                }

                try:

                    archivo_mat.operar_canales(
                        funciones[operacion],
                        canales,
                        punto_min,
                        punto_max,
                        epoca
                    )

                except Exception as error:
                    print(
                        "\nError en la operación:",
                        error
                    )

    # ==========================================
    # ESTADÍSTICAS MATRIZ 3D
    # ==========================================

    elif opcion == 9:

        if archivo_mat is None:
            print(
                "\nPrimero debe cargar un archivo MAT."
            )

        else:

            print(
                "\nLos ejes disponibles son 0, 1 y 2."
            )

            eje1 = validar_entero(
                "Primer eje: ",
                0,
                2
            )

            eje2 = validar_entero(
                "Segundo eje: ",
                0,
                2
            )

            if eje1 == eje2:

                print(
                    "\nLos ejes deben ser diferentes."
                )

            else:

                try:

                    archivo_mat.estadisticas_3d(
                        eje1,
                        eje2
                    )

                except Exception as error:
                    print(
                        "\nError al calcular estadísticas:",
                        error
                    )

    # ==========================================
    # LISTAR OBJETOS ALMACENADOS
    # ==========================================

    elif opcion == 10:

        print("\n" + str(gestor))


    # ==========================================
    # BUSCAR OBJETO
    # ==========================================

    elif opcion == 11:

        nombre = input(
            "\nIngrese el nombre del objeto a buscar: "
        ).strip()

        objeto = gestor.buscar(nombre)

        if objeto is None:
            print("\nNo se encontró un objeto con ese nombre.")

        else:
            print("\nObjeto encontrado:")
            print("Nombre:", nombre)
            print("Tipo:", type(objeto).__name__)
            print("\nInformación:")
            print(objeto)
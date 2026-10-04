from clases import ArchivoMAT


archivo_mat = ArchivoMAT(
    "datos/Archs_MAT/Sensitive_Cue.mat"
)

promedio, desviacion = archivo_mat.estadisticas_3d(
    eje1=1,
    eje2=2
)
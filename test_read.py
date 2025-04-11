from read_gpt import leer_hoja_gpt

datos = leer_hoja_gpt()

# Mostrar las primeras 3 filas
for fila in datos[:3]:
    print(fila)

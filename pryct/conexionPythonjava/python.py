import json
# sys: Librería con funciones y variables para manipular el entorno de ejecución.
import sys
# sys.stdin: Utilizado para ingreso interactivo de datos
# sys.stdin.readline(): Lee el contenido ingresado hasta que encuentra el carácter de salto de línea, o sea, hasta que se presiona saltar.
nombre = sys.stdin.readline()
# print(): Imprime datos en pantalla. Cuando Python es ejecutado como un subproceso, envía los datos al programa que invocó a Python.
c = "hola" + nombre

respuesta = {
    "felicidad" : [", saludos desde el python", "jaja este no"],
    "bn" : "hola" + nombre
}
print(json.dumps(respuesta))
# sys.stdout.flush(): Fuerza la salida de datos del buffer
sys.stdout.flush()
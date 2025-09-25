import os
import shutil



#HAY QUE CAMBIAR LA FUNCION MOVER PARA QUE LA NUEVA UBICACION NO SEA IDENTIFICADORCARP1



"""
# Importamos Flask para crear el servidor web, request para leer el cuerpo de la petición
# y jsonify para devolver respuestas en formato JSON fácilmente.
from flask import Flask, request, jsonify

# CORS permite que el navegador del frontend (que puede estar en otro origen/puerto)
# pueda hacer peticiones a este backend. Sin CORS, el navegador las bloquearía.
from flask_cors import CORS

# Creamos la aplicación Flask.
app = Flask(__name__)

# Habilitamos CORS globalmente (para todas las rutas). En producción conviene
# restringirlo a los orígenes que realmente vayan a usar tu API.
CORS(app)
@app.route("/prompt", methods=["POST"])
def consiguePromt():
    prompt = request.get_json()
    interpreta(prompt)
 
"""

#variables para que el back sepa que hacer
functionToBeDone = "mover"
srccc = True           #¿el src de la carpeta esta completo o no?
ntpo = False        #¿el identificador del archivo es el nombre/vinculo o el tipo de archivo?
identificadorArch1 = [""] #el archivo principal que sera modificado, o la forma de encontrar los archivos
identificadorArch2 = "" #en caso de involucrar un segundo archivo
identificadorCarp1 = "C:/Users/52218824/Documents/GitHub/A.T.L.A.S/bcknd2" #será la carpeta en la que se encuentra en archivo
identificadorCarp2 = "C:\\Users\\52218824\\Documents\\GitHub\\A.T.L.A.S\\bcknd" #en caso de involucrar 2 carpetas
txt1 = " con gloria " #en caso de involucrar un texto, se usara este, en funciones de agregar, eleminar, o reemplazar, es el texto que viene antes del agregado y/o el que hay que eliminar
txt2 = ", en realidad me cae mal gloria" #en caso de involucrar 2, este tambien
walk = True #Todos los archivos solo dentro de una carpeta? o dentro de sus subcarpetas tambien?
lineaAntes = True
lineaDespues = True

def interpreta(prompt):
    #interpretacion
    global identificadorCarp1, identificadorCarp2, identificadorArch1, identificadorArch2
    print("dd")
    archivo_s = []
    if(identificadorCarp1 != "" and identificadorCarp1[0] != "C"):
        print("encontrand carpeta por nombre")
        identificadorCarp1 = encontrarCarPorNombre(identificadorCarp1)
        print("carpeta 1 identificada")
        print(identificadorCarp1)
    else:
        print(identificadorCarp1)
    if(identificadorCarp2 != "" and identificadorCarp2[0] != "C"):
        print(identificadorCarp2 + "\n")
        identificadorCarp2 = encontrarCarPorNombre(identificadorCarp2)
        print(identificadorCarp2)

    if(ntpo == False):
        if(walk == True):
            print(f"encontrando archivos tipo {identificadorArch1} en subcarpetas de {identificadorCarp1}")
            
            for i in range(len(identificadorArch1)):
                papa =  walkCarp(identificadorArch1[i], identificadorCarp1)
                for f in range(len(papa)):
                    archivo_s.append(papa[f])
            print("linea 54")
        else:
            print(f"encontrando archivos tipo {identificadorArch1} en {identificadorCarp1}")
            archivo_s = encontrartipoencarpeta(identificadorArch1[0], identificadorCarp1)
            print("linea 58")
    elif(identificadorArch1[0] != "C" and functionToBeDone != "crea"):
        print(f"buscando archivos de nombre {identificadorArch1}")
        archivo_s = encontrArchPorNombre(identificadorArch1[0])
        print("linea 62")
    else:
        archivo_s = identificadorArch1
        print("linea 66")
    print(archivo_s)
    x = len(archivo_s)
    print("identificado")
    if(functionToBeDone == "crea"):
        for i in range(x):
            crea(txt1, archivo_s[i])
    elif(functionToBeDone == "modificaDondeDice"):
        print(functionToBeDone)
        for i in range(x):
            modificaDondeDice(txt2, archivo_s[i],  txt1, lineaAntes, lineaDespues)
    elif(functionToBeDone == "sacarLoQueDice"):
        for i in range(x):
            sacarLoQueDice(archivo_s[i], txt1)
    elif(functionToBeDone == "reemplazar"):
        for i in range(x):
            reemplazar(txt2, archivo_s[i], txt1)
    elif(functionToBeDone == "eliminARchivo"):
        for i in range(x):
            eliminARchivo(archivo_s[i])
    elif(functionToBeDone == "copiar"):
        for  i in range(x):
            copiar(archivo_s[i], identificadorCarp2)
    elif(functionToBeDone == "mover"):
        for i in  range(x):
            mover(archivo_s[i], identificadorCarp2)



"""
Funciones de manejo de archivos:
"""
def crea(txtAgregar, archivo):
    try:
        with open(archivo, 'x') as e:
            e.write(txtAgregar)
    except ValueError:
        return("Error de formato")
    except FileExistsError:
        return(f"El archivo {archivo} ya existe")

def modificaDondeDice(txtAgregar, archivo, ubicacionenArchivo, lineaAntes, lineaDespues):
    nts = ""
    dsps = ""
    if(lineaAntes == True):
        nts = " \n "
    if(lineaDespues == True):
        dsps = " \n "
    reemplazar(txtAgregar, archivo, nts + txtAgregar + dsps)



def sacarLoQueDice(archivo, ubicacionenArchivo):
    reemplazar("", archivo, ubicacionenArchivo)

def reemplazar(txtNuevo, archivo, ubicacionenArchivo):
    print(f"intentando sacar {ubicacionenArchivo} de {archivo}")
    try:
        cocos = ""
        with open(archivo, 'r') as e:
            cocos = e.read()
            print(cocos)
    except FileNotFoundError:
        print(f"El archivo {archivo} no existe")
        return(f"El archivo {archivo} no existe")
    except ValueError:
        print(ValueError)
        return("Error de formato")
    ubccionmbr = cocos.replace(ubicacionenArchivo, txtNuevo)
    print(ubccionmbr)
    if(ubccionmbr != cocos):
        with open(archivo, 'w') as f:
            f.write(ubccionmbr)
            print("listo")
            return(200)
    else:
        print("\n En ningun lado el archivo dice eso \n")
        return("En ningun lado el archivo dice eso")

def eliminARchivo (archivo):
    if(os.path.exists(archivo)):
        os.remove(archivo)
    else:
        print("\n jaja no existeeeeee el archivo ese tuyo\n ")
        return("archivo no existe")

def copiar(archivo, nuevaUbicacion):
    try:
        shutil.copy(archivo, nuevaUbicacion)
    except FileExistsError:
        print("Repetido")

def mover(archivoM, nuevaUbicacionM):
    try:
        shutil.move(archivoM, nuevaUbicacionM)
    except shutil.Error as e:
        print(f"Carpeta repetida")
    

def encontrartipoencarpeta(terminacion, carpeta):
    try:
        nombres = os.listdir(carpeta)
        nombresTrmncion = []
        for i in range(len(nombres)):
            posicioNombre = nombres[i].rfind(".")
            if(nombres[i][posicioNombre:] == terminacion):
                nombresTrmncion.append(nombres[i])
        if(nombresTrmncion == []):
            print(f"No se ha encontrado ningun archivo con la terminacion {terminacion}")
            return(f"No se ha encontrado ningun archivo con la terminacion {terminacion}")
        return nombresTrmncion
    except FileNotFoundError:
        print("La carpeta que busca no existe")
    except ValueError:
        print(ValueError)
listerminaciones = []
compatible = False

def terminacionCompatible(archivo):
    a = archivo.rfind(".")
    terminacion = archivo[a + 1:]
    compatible = False
    for i in range(len(listerminaciones)):
        if(terminacion == listerminaciones[i]):
            compatible = True
    return compatible


def encontrArchPorNombre(archivo):
     for (root,dirs,files) in os.walk('C:\\', topdown=True):
        for i in range(len(files)):
             if(files[i] == archivo):
                return [os.path.join(root, files[i])]

def encontrarCarPorNombre(carpeta):
    for(root, dirs, files) in os.walk('C:\\', topdown=True):
        for i in range(len(dirs)):
            if(dirs[i] == carpeta):
                return os.path.join(root, dirs[i]) + "\\"

def walkCarp(terminacion, carpeta):
    carpeta = carpeta.replace("/", "\\")
    rutas: list[str] = []
    for (root,dirs,files) in os.walk(carpeta, topdown=True):
        for i in range(len(files)):
            posicioNombre = files[i].rfind(".")
            if(files[i][posicioNombre:] == terminacion or (terminacion == "")):
                rutas.append(os.path.join(root, files[i]))
    if(rutas == []):
        print(f"no se encontró ningún archivo tipo {terminacion}")
    else:
        return(rutas)


def dupdic(carvieja, carnueva):
    shutil.copytree(carvieja, carnueva)
    """
    for(root, files, dirs) in os.walk(carvieja, topdown = True):
        for i in range(len(dirs)):
            a = os.path.join(root, dirs[i])
            b = a.replace(carvieja, carnueva)
            b = b[:b.rfind("\\")]
            shutil.copy(a, b)
        for i in range(len(files)):
            a = os.path.join(root, files[i])
            b = a.replace(carvieja, carnueva)
            b = b[:b.rfind("\\")]
            shutil.copy(a, b)
        """
dupdic("C:\\Users\\52218824\\Documents\\GitHub\\A.T.L.A.S\\pryct", "C:\\Users\\52218824\\Documents\\GitHub\\A.T.L.A.S\\pryct2")


"""
# Punto de entrada del programa. Si ejecutas `python app.py`, Flask levanta el servidor local.
if __name__ == "__main__":
    # debug=True recarga el servidor al detectar cambios y muestra trazas de error legibles.
    # port=5000 hace que escuche en http://127.0.0.1:5000
    app.run(port=5000, debug=True)
"""
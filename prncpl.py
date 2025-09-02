import os
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

def interpreta(prompt):
    #interpretacion
    archivo_s = []
    if(identificadorCarp1 != "" and identificadorCarp1[0] != "C"):
        identificadorCarp1 = encontrarCarPorNombre(identificadorCarp1)
    if(identificadorCarp2 != "" and identificadorCarp2[0] != "C"):
        identificadorCarp2 = encontrarCarPorNombre(identificadorCarp2)

    if(identificadorArch1[0] == "."):
        if(walk == True):
            archivo_s = walkCarp(identificadorArch1, identificadorCarp1)
        else:
            archivo_s = encontrartipoencarpeta(identificadorArch1, identificadorCarp1)
    elif(identificadorArch1[0] != "C"):
        archivo_s = encontrArchPorNombre(identificadorArch1)
    x = len(archivo_s)
    if(functionToBeDone == "crea"):
        for i in range(x):
            crea(txt1, archivo_s[i])
    elif(functionToBeDone == "modificaDondedice"):
        for i in range(x):
            modificaDondedice(txt2, archivo_s[i],  txt1, lineaAntes, lineaDespues)
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
            copiar(archivo_s[i], identificadorCarp1)
    elif(functionToBeDone == "mover"):
        for i in  range(x)::
            mover(archivo_s[i], identificadorCarp1)



"""
Funciones de manejo de archivos:
"""
def crea(txtAgregar, archivo):
    try:
        with open(archivo, 'x') as e:
            e.write(txtAgregar)
    except ValueError:
        print("txtAgregar no es texto")
        return
    except FileExistsError:
        print(f"El archivo {archivo} ya existe")
        return

def modificaDondedice(txtAgregar, archivo, ubicacionenArchivo, lineaAntes, lineaDespues):
    nts = ""
    dsps = ""
    if(lineaAntes == True):
        nts = "\n"
    if(lineaDespues == True):
        dsps = "\n"
    chueco = ""
    if not (isinstance(lineaAntes, bool) or isinstance(lineaDespues, bool)):
        print("Lineantes o LineaDespues no son bool")
        return
    try:
        with open(archivo, 'r') as e:
            chueco = e.read()
    except FileNotFoundError:
        print(f"El archivo {archivo} no existe")
        return
    except ValueError:
        print(ValueError)
        return
    ubccionmbr = chueco.find(ubicacionenArchivo)
    if(ubccionmbr != -1):
        before =  chueco[:ubccionmbr + len(ubicacionenArchivo)]
        after = chueco[ubccionmbr + len(ubicacionenArchivo):]
        
        with open(archivo, 'w') as f:
            f.write(before + nts + txtAgregar + dsps + after)
    else:
        print("\n No exite esa parte del texto \n")
        return



def sacarLoQueDice(archivo, ubicacionenArchivo):
    print(f"intentando sacar {ubicacionenArchivo} de {archivo}")
    try:
        cocos = ""
        with open(archivo, 'r') as e:
            cocos = e.read()
            print(cocos)
    except FileNotFoundError:
        print(f"El archivo {archivo} no existe")
        return
    except ValueError:
        print(ValueError)
        return 
    ubccionmbr = cocos.find(ubicacionenArchivo)
    print(ubccionmbr)
    if(ubccionmbr != -1):
        before = cocos[:ubccionmbr]
        after = cocos[ubccionmbr + len(ubicacionenArchivo):]
        print(before)
        print(after)
        print("solo hace falta reescribir el archivo")
        with open(archivo, 'w') as f:
            f.write(before + after)
            print("listo")
    else:
        print("\n En ningun lado el archivo dice eso \n")
        return

def reemplazar(txtNuevo, archivoR, txtViejo):
    modificaDondedice(txtNuevo, archivoR, txtViejo, False, False)
    sacarLoQueDice(archivoR, txtViejo)

def eliminARchivo (archivo):
    if(os.path.exists(archivo)):
        os.remove(archivo)
    else:
        print("\n jaja no existeeeeee el archivo ese tuyo\n \n ")

def copiar(archivo, nuevaUbicacion):
    chueco = ""
    posicioNombre = archivo.rfind("/")
    nombre = archivo[posicioNombre + 1:]
    try:
        with open(archivo, 'r') as e:
            chueco = e.read()
    except FileNotFoundError:
        print("\n No existe el archivo indicado")
    try:
        with open(nuevaUbicacion + nombre, 'x') as f:
            f.write(chueco)
    except FileExistsError:
        print("\n La copia que desea generar ya existe")

def mover(archivoM, nuevaUbicacionM):
    copiar(archivoM, nuevaUbicacionM)
    eliminARchivo(archivoM)

def encontrartipoencarpeta(terminacion, carpeta):
    try:
        nombres = os.listdir(carpeta)
        nombresTrmncion = []
        for i in range(len(nombres)):
            posicioNombre = nombres[i].rfind(".")
            if(nombres[i][posicioNombre:] == terminacion):
                nombresTrmncion.append(nombres[i])
        if(nombresTrmncion == []):
            print("No se ha encontrado ningun archivo con el nombre deseado")
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
                return os.path.join(root, dirs[i])

def terminacionEnDisco(terminacion):
    rutas: list[str] = []
    for (root,dirs,files) in os.walk('C:\\', topdown=True):
        for i in range(len(files)):
            posicioNombre = files[i].rfind(".")
            if(files[i][posicioNombre:] == terminacion):
                rutas.append(os.path.join(root, files[i]))
    if(rutas == []):
        print(f"no se encontró ningún archivo tipo {terminacion}")
    else:
        return(rutas)


#variables para que el back sepa que hacer
functionToBeDone = None
srcc = False            #¿el src esta completo o no?
identificadorArch1 = "" #el archivo principal que sera modificado, o la forma de encontrar los archivos
identificadorArch2 = "" #en caso de involucrar un segundo archivo
identificadorCarp1 = "" #será la carpeta en la que se encuentra en archivo
identificadorCarp2 = "" #en caso de involucrar 2 carpetas
txt1 = "" #en caso de involucrar un texto, se usara este
txt2 = "" #en caso de involucrar 2, este tambien
walk = False
lineaAntes = ""
lineaDespues = ""

"""
# Punto de entrada del programa. Si ejecutas `python app.py`, Flask levanta el servidor local.
if __name__ == "__main__":
    # debug=True recarga el servidor al detectar cambios y muestra trazas de error legibles.
    # port=5000 hace que escuche en http://127.0.0.1:5000
    app.run(port=5000, debug=True)
"""
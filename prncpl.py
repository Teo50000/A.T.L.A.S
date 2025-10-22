import os
import shutil



from pypdf import PdfReader
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet

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
disco = "C" #por default se trabajará en el disco C, si se desea cambiarlo se puede
functionToBeDone = "crea"
srccc = True        #¿el src de la carpeta esta completo o no?
ntpo = True       #¿el identificador del archivo es el nombre/vinculo o el tipo de archivo?
identificadorArch1 = ["noo:ssda.txt", "ESTEESTABIEN.txt"] #el archivo principal que sera modificado, o la forma de encontrar los archivos
identificadorArch2 = "" #en caso de involucrar un segundo archivo
identificadorCarp1 = "C:/Users/52218824/Documents/GitHub/A.T.L.A.S/" #será la carpeta en la que se encuentra en archivo
identificadorCarp2 = "C:/Users/52218824/" #en caso de involucrar 2 carpetas
txt1 = "aertyu" #en caso de involucrar un texto, se usara este, en funciones de agregar, eleminar, o reemplazar, es el texto que viene antes del agregado y/o el que hay que eliminar
txt2 = "YZ" #en caso de involucrar 2, este tambien
walk = False #Todos los archivos solo dentro de una carpeta? o dentro de sus subcarpetas tambien?
lineaAntes = False
lineaDespues = False

#esta se usa solo en archivoAaPDF y PDFaTexto
nombres = ["hola", "adios", "REPÚBLICA DEMOCRÁTICA Y POPULAR DE COREA"]   #no usar variable a menos que sea estrictamente necesario
replicar = True
terminacion = ".txt"

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
    if(functionToBeDone != "dupdic"):
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
        elif(srccc == False and (functionToBeDone != "crea" or functionToBeDone != "pdf")):
            print(f"buscando archivos de nombre {identificadorArch1}")
            for i in range(len(identificadorArch1)):
                archivo_s.append(encontrArchPorNombre(identificadorArch1[i]))
            print("linea 62")
        else:
            archivo_s = identificadorArch1
            print("linea 66")
        print(archivo_s)
        x = len(archivo_s)
    print("identificado")
    if(functionToBeDone == "crea"):
        for i in range(x):    
            bienescrito = True
            aVerNoPodesPonerEsosCaracteresPoneAlgoNormal = ["$", "/", ":", '"', "<", ">", "|", "?", "*", "\\"]
            for f in range(len(aVerNoPodesPonerEsosCaracteresPoneAlgoNormal)):
                if aVerNoPodesPonerEsosCaracteresPoneAlgoNormal[f] in archivo_s[i]:
                    bienescrito = False
            crea(txt1, identificadorCarp1 + archivo_s[i]) if  bienescrito else print("PONE UN CARACTER NORMAL")
    elif(functionToBeDone == "pdf"):
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
        print("reemplazando")
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
    elif(functionToBeDone == "dupdic"):
        dupdic(identificadorCarp1, identificadorCarp2)
    elif(functionToBeDone == "movdic"):
        movdic(identificadorCarp1, identificadorCarp2)
    elif(functionToBeDone == "buscarSRC"):
        return(archivo_s)
    elif(functionToBeDone == "archivoAaPDF"):
        if(replicar == True):
            for i in range(x):
                rew = archivo_s[i]
                ultimaBarra = rew.rfind("\\")
                nombrigual = rew[ultimaBarra+2: - len(terminacion)]
                rutigual = rew[:ultimaBarra+2]
                archivoAaPDF(rew, nombrigual, rutigual)
        else:
            for i in  range(x):
                archivoAaPDF(archivo_s[i], nombres[i], identificadorCarp2)
    elif(functionToBeDone == "PDFaTexto"):
        if(replicar == True):
            for i in range(x):
                rew = archivo_s[i]
                ultimaBarra = rew.rfind("\\")
                nombrigual = rew[ultimaBarra+2: - 4] + terminacion
                rutigual = rew[:ultimaBarra+2]
                PDFaTexto(rew, nombrigual, rutigual)
        else:
            for i in  range(x):
                archivoAaPDF(archivo_s[i], nombres[i], identificadorCarp2)
    elif(functionToBeDone == "renombrar"):
        renombrar(archivo_s[i], identificadorArch2)



"""
Funciones de manejo de archivos:
"""
def crea(txtAgregar, archivo):

    try:
        with open(archivo, 'x', encoding = 'utf-8') as e:
            e.write(txtAgregar)
    except ValueError:
        return("Error de formato")
    except FileExistsError:
        print(f"El archivo {archivo} ya existe")
        return(f"El archivo {archivo} ya existe")

def modificaDondeDice(txtAgregar, archivo, ubicacionenArchivo, lineaAntes, lineaDespues):
    nts = ""
    dsps = ""
    if(lineaAntes == True):
        nts = " \n"
        print(nts)
        print("texto:" + nts + txtAgregar)
    if(lineaDespues == True):
        dsps = "\n "
    reemplazar( ubicacionenArchivo + nts + txtAgregar + dsps, archivo, ubicacionenArchivo)



def sacarLoQueDice(archivo, ubicacionenArchivo):
    reemplazar("", archivo, ubicacionenArchivo)

def reemplazar(txtNuevo, archivo, ubicacionenArchivo):
    print(f"intentando sacar {ubicacionenArchivo} de {archivo}")
    try:
        cocos = ""
        with open(archivo, 'r', encoding = 'utf-8') as e:
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
        with open(archivo, 'w', encoding = 'utf-8') as f:
            f.write(ubccionmbr)
            print("listo")
            return(200)
    else:
        print(f"\n En ningun lado el archivo dice eso {ubicacionenArchivo}\n")
        return("En ningun lado el archivo dice eso")

def eliminARchivo (archivo):
    if(os.path.exists(archivo)):
        os.remove(archivo)
    else:
        print("\n jaja no existeeeeee el archivo ese tuyo\n ")
        return("archivo no existe")

def copiar(archivo, nuevaUbicacion):
    if not os.path.exists(nuevaUbicacion):
        print(f"no existe {nuevaUbicacion}")
        return(f"no existe {nuevaUbicacion}")
    try:
        shutil.copy(archivo, nuevaUbicacion)
    except FileNotFoundError:
        print("no existe archivo")
    except FileExistsError:
        print("Repetido")

def mover(archivoM, nuevaUbicacionM):
    if not os.path.exists(nuevaUbicacionM):
        print(f"no existe {nuevaUbicacionM}")
        return(f"no existe {nuevaUbicacionM}")

    try:
        shutil.move(archivoM, nuevaUbicacionM)
    except FileNotFoundError:
        print("no existe archivo")
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
    global disco
    for (root,dirs,files) in os.walk(f"{disco}:\\", topdown=True):
        for i in range(len(files)):
             if(files[i] == archivo):
                return os.path.join(root, files[i])

def encontrarCarPorNombre(carpeta):
    global disco
    for(root, dirs, files) in os.walk(f"{disco}:\\", topdown=True):
        for i in range(len(dirs)):
            if(dirs[i] == carpeta):
                return os.path.join(root, dirs[i]) + "\\"

def walkCarp(terminacion, carpeta):
    if not os.path.exists(carpeta):
        print(f"no existe {carpeta}")
        return(f"no existe {carpeta}")
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
    if not os.path.exists(carvieja):
        print(f"no existe {carvieja}")
        return(f"no existe {carvieja}")
    if not os.path.exists(carnueva):
        print(f"no existe {carnueva}")
        return(f"no existe {carnueva}")
    try:
        shutil.copytree(carvieja, carnueva)
    except FileNotFoundError:
        print("no existe archivo")

def movdic(carvieja, carnueva):
    if not os.path.exists(carvieja):
        print(f"no existe {carvieja}")
        return(f"no existe {carvieja}")
    if not os.path.exists(carnueva):
        print(f"no existe {carnueva}")
        return(f"no existe {carnueva}")
    try:
        dupdic(carvieja, carnueva)
        shutil.rmtree(carvieja)
    except FileNotFoundError:
        print("no existe archivo")

def leer(archivo):
    try:
        cocos = ""
        with open(archivo, 'r', encoding = 'utf-8') as e:
            cocos = e.read()
            return(cocos)
    except FileNotFoundError:
        print(f"El archivo {archivo} no existe")
        return(FileNotFoundError)
    except ValueError:
        print(ValueError)
        return(ValueErrorr)

def pdf(text, nombre, ruta):
    # Crear un documento PD F nuevo
    aVerNoPodesPonerEsosCaracteresPoneAlgoNormal = ["$", "/", ":", '"', "<", ">", "|", "?", "*", "\\"]
    for f in range(len(aVerNoPodesPonerEsosCaracteresPoneAlgoNormal)):
        if aVerNoPodesPonerEsosCaracteresPoneAlgoNormal[f] in nombre:
            print("PONE UN NOMBRE NORMAL")
            return("pone un nombnre normal")
    nombre = ruta + nombre + ".pdf"
    if(os.path.exists(nombre)):
        print("ya existe")
        return("Ya existe")
    doc = SimpleDocTemplate(nombre, pagesize=letter)

    # Estilos para el párrafo
    styles = getSampleStyleSheet()
    style = styles["Normal"]

    # Reemplazar saltos de línea con etiquetas HTML para que se respeten
    # (Paragraph interpreta el texto como HTML-lite)
    if text:
        text = text.replace('\n', '<br/>')
        text = text.replace('\t', '&nbsp;&nbsp;&nbsp;&nbsp;')  # HTML-safe espacio
    else:
        text = "No hay texto"

    # Crear contenido
    content = []
    content.append(Paragraph(text, style))
    content.append(Spacer(1, 12))  # Espacio opcional entre párrafos

    # Construir el PDF
    doc.build(content)

    print(f"PDF creado: {nombre}")


def archivoAaPDF(archivo, nuevoNombre, ruta):
    texto = leer(archivo)
    pdf(texto, nuevoNombre, ruta)

def leerPDF(archivo):
    reader = PdfReader(archivo)
    number_of_pages = len(reader.pages)
    text = ""
    for i in range(number_of_pages):
        text = text + reader.pages[i].extract_text()
        
    print(text)
    return text

def PDFaTexto(pdf, nuevoNombre, ruta):
    texto = leerPDF(pdf)
    crea(texto, ruta + nuevoNombre)

def renombrar(archV, nuevoNombre):
    archV.replace("/", "\\")
    ultBar = archV.rfind("\\")
    nuevoNombre = archV[:ultBar + 1] + nuevoNombre
    if(os.path.exists(nuevoNombre)):
        print("no se puede")
        return("ya existe")
    os.rename(archV, nuevoNombre)
    print(nuevoNombre)

archivoAaPDF("antártica_experimento.txt", "asdf.ASDF-ASDFGH_UYTREWS;", "./")
"""
# Punto de entrada del programa. Si ejecutas `python app.py`, Flask levanta el servidor local.
if __name__ == "__main__":
    # debug=True recarga el servidor al detectar cambios y muestra trazas de error legibles.
    # port=5000 hace que escuche en http://127.0.0.1:5000
    app.run(port=5000, debug=True)
"""
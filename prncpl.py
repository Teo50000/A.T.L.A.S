import os
import shutil



#from pypdf import PdfReader
#from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
#from reportlab.lib.pagesizes import letter
#from reportlab.lib.styles import getSampleStyleSheet

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
functionToBeDone = "sacarLoQueDice"
srccc = True          #¿el src de la carpeta esta completo o no?
ntpo = True        #¿el identificador del archivo es el nombre/vinculo o el tipo de archivo?
identificadorArch1 = ["C:/Users/52218824/Documents/GitHub/A.T.L.A.S/nose.txt"] #el archivo principal que sera modificado, o la forma de encontrar los archivos
identificadorArch2 = "corrupto.docx" #en caso de involucrar un segundo archivo
identificadorCarp1 = "C:/Users/52218824/Documents/GitHub/A.T.L.A.S/" #será la carpeta en la que se encuentra en archivo
identificadorCarp2 = "C:/Users/52218824/Favorites/" #en caso de involucrar 2 carpetas
txt1 = ", educacion, patria, y familiasalud" #en caso de involucrar un texto, se usara este, en funciones de agregar, eleminar, o reemplazar, es el texto que viene antes del agregado y/o el que hay que eliminar
txt2 = "salud" #en caso de involucrar 2, este tambien
walk = True #Todos los archivos solo dentro de una carpeta? o dentro de sus subcarpetas tambien?
lineaAntes = False
lineaDespues = False

#esta se usa solo en archivoAaPDF y PDFaTexto
nombres = ["A A A A AA", "A C I C U L I F O L I O", "E S C L E R O F I L O", "LEOLECIEELEYULAVIIIIIIIIIII", "....pdf...pdf.pdf.pdf.pdf.pdf"]   #no usar variable a menos que sea estrictamente necesario
replicar = True
terminacion = ".js"

def interpreta(prompt):
    #interpretacion
    global identificadorCarp1, identificadorCarp2, identificadorArch1, identificadorArch2
    identificadorCarp1 = identificadorCarp1.replace("/", "\\")
    identificadorCarp2 = identificadorCarp2.replace("/", "\\")
    print(f"\n idenitificadorcarp1: {identificadorCarp1} \n identificadorcarp2: {identificadorCarp2} \n")
    try:
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
                    if(type(archivo_s) == str):
                        return archivo_s
                    print("linea 58")
            elif(srccc == False and functionToBeDone != "crea" and functionToBeDone != "pdf"):
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
            for i in range (x):
                renombrar(archivo_s[i], identificadorArch2)
    except Exception:
        raise


"""
Funciones de manejo de archivos:
"""
def crea(txtAgregar, archivo):

    try:
        with open(archivo, 'x', encoding = 'utf-8') as e:
            e.write(txtAgregar)
    except ValueError:
        raise ValueError("Error de formato-crea")
    except FileExistsError:
        print(f"El archivo {archivo} ya existe")
        raise FileExistsError(f"El archivo {archivo} ya existe-crea")

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
        raise FileNotFoundError(f"El archivo {archivo} no existe-reemplazar")
    except ValueError:
        print(ValueError)
        raise ValueError("Error de formato-reemplazar")
    ubccionmbr = cocos.replace(ubicacionenArchivo, txtNuevo)
    print(ubccionmbr)
    if(ubccionmbr != cocos):
        with open(archivo, 'w', encoding = 'utf-8') as f:
            f.write(ubccionmbr)
            print("listo")
            return(200)
    else:
        print(f"\n En ningun lado el archivo dice eso {ubicacionenArchivo}\n")
        raise Exception("En ningun lado el archivo dice eso-reemplazar")

def eliminARchivo (archivo):
    if(os.path.exists(archivo)):
        os.remove(archivo)
    else:
        print("\n jaja no existeeeeee el archivo ese tuyo\n ")
        raise FileNotFoundError("archivo no existe-eliminARchivo")

def copiar(archivo, nuevaUbicacion):
    if not os.path.exists(nuevaUbicacion):
        print(f"no existe {nuevaUbicacion}")
        raise FileNotFoundError(f"no existe la ubicación {nuevaUbicacion}-copiar")
    try:
        shutil.copy(archivo, nuevaUbicacion)
    except FileNotFoundError:
        print("no existe archivo-copiar")
    except FileExistsError:
        print("Copia ya existente-copiar")

def mover(archivoM, nuevaUbicacionM):
    if not os.path.exists(nuevaUbicacionM):
        print(f"no existe {nuevaUbicacionM}")
        raise FileNotFoundError(f"no existe la nueva ubicación {nuevaUbicacionM}-mover")

    try:
        shutil.move(archivoM, nuevaUbicacionM)
    except FileNotFoundError:
        print("no existe archivo")
        raise FileNotFoundError("No existe el archivo-mover")
    except shutil.Error as e:
        print(f"Carpeta repetida")
        raise shutil.Error("Carpeta repetida-mover")
    

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
            raise Exception(f"No se ha encontrado ningun archivo con la terminacion {terminacion}-encontrartipoencarpeta")
        return nombresTrmncion
    except FileNotFoundError:
        print("La carpeta que busca no existe")
        raise FileNotFoundError("La carpeta que busca no existe-emcontrartipoencarpeta")
    except ValueError:
        print(ValueError)
        raise ValueError("ValueError-encontrartipoencarpeta")
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
        raise FileNotFoundError(f"no existe {carpeta}-walkCarp")
    # hacer carpeta = carpeta.replace("/", "\\") ya no hace falta
    rutas: list[str] = []
    for (root,dirs,files) in os.walk(carpeta, topdown=True):
        for i in range(len(files)):
            posicioNombre = files[i].rfind(".")
            if(files[i][posicioNombre:] == terminacion or (terminacion == "")):
                rutas.append(os.path.join(root, files[i]))
    if(rutas == []):
        print(f"no se encontró ningún archivo tipo {terminacion}")
        raise Exception(f"no se encontró ningún archivo tipo {terminacion}-walkCarp")
    else:
        return(rutas)


def dupdic(carvieja, carnueva):
    print(carvieja)
    print(carnueva)
    if not os.path.exists(carvieja):
        print(f"no existe {carvieja}")
        raise FileNotFoundError(f"no existe carpeta origen {carvieja}-dupdic")
    if not os.path.exists(carnueva):
        print(f"no existe {carnueva}")
        raise FileNotFoundError(f"no existe carpeta destino {carnueva}-dupdic")
    ultBar = carvieja.rfind("\\")
    antultbarra = carvieja.rfind("\\", 0, ultBar)
    nombre = carvieja[antultbarra + 1:]
    carnueva = carnueva + nombre
    print(carnueva)
    try:
        shutil.copytree(carvieja, carnueva)
    except FileNotFoundError:
        print("no existe archivo")
    except FileExistsError:
        print("Copia ya existe")
        raise FileExistsError(f"Copia de {carvieja} ya existente en {carnueva}-dupdic")

def movdic(carvieja, carnueva):
    try:
        dupdic(carvieja, carnueva)
        shutil.rmtree(carvieja)
    except Exception:
        raise

def leer(archivo):
    try:
        cocos = ""
        with open(archivo, 'r', encoding = 'utf-8') as e:
            cocos = e.read()
            return(cocos)
    except FileNotFoundError:
        print(f"El archivo {archivo} no existe")
        raise FileNotFoundError(f"El archivo {archivo} no existe-leer")
    except ValueError:
        print(ValueError)
        raise ValueError("ValueError-leer")

"""
def pdf(text, nombre, ruta):
    # Crear un documento PD F nuevo
    aVerNoPodesPonerEsosCaracteresPoneAlgoNormal = ["$", "/", ":", '"', "<", ">", "|", "?", "*", "\\"]
    for f in range(len(aVerNoPodesPonerEsosCaracteresPoneAlgoNormal)):
        if aVerNoPodesPonerEsosCaracteresPoneAlgoNormal[f] in nombre:
            print("PONE UN NOMBRE NORMAL")
            raise ValueError("pone un nombnre normal - pdf")
    nombre = ruta + nombre + ".pdf"
    if(os.path.exists(nombre)):
        print("ya existe")
        raise FileExistsError("Ya existe pdf-pdf")
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
        raise Exception("no hay texto-pdf")

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
    try:
        reader = PdfReader(archivo)
        number_of_pages = len(reader.pages)
        text = ""
        for i in range(number_of_pages):
            text = text + reader.pages[i].extract_text()
            
        print(text)
        return text
    except ValueError:
        raise ValueError("ValueError-leerPDF")
    except FileNotFoundError:
        raise FileNotFoundError("PDF no existente-leerPDF")

def PDFaTexto(pdf, nuevoNombre, ruta):
    texto = leerPDF(pdf)
    crea(texto, ruta + nuevoNombre)
"""
def renombrar(archV, nuevoNombre):
    archv = archV.replace("/", "\\")
    ultBar = archV.rfind("\\")
    nuevoNombre = archV[:ultBar + 1] + nuevoNombre
    if not os.path.exists(archV):
        raise FileNotFoundError(f"El archivo {archV} no existe-renombrar")
    if(os.path.exists(nuevoNombre)):
        print("no se puede")
        raise FileExistsError("ya existe")
    os.rename(archV, nuevoNombre)
    print(nuevoNombre)


"""
# Punto de entrada del programa. Si ejecutas `python app.py`, Flask levanta el servidor local.
if __name__ == "__main__":
    # debug=True recarga el servidor al detectar cambios y muestra trazas de error legibles.
    # port=5000 hace que escuche en http://127.0.0.1:5000
    app.run(port=5000, debug=True)
"""

interpreta(5)
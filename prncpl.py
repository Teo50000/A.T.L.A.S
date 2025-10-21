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
functionToBeDone = "archivoAaPDF"
srccc = False        #¿el src de la carpeta esta completo o no?
ntpo = False       #¿el identificador del archivo es el nombre/vinculo o el tipo de archivo?
identificadorArch1 = [".txt"] #el archivo principal que sera modificado, o la forma de encontrar los archivos
identificadorArch2 = "" #en caso de involucrar un segundo archivo
identificadorCarp1 = "C:/Users/52218824/Documents/GitHub/A.T.L.A.S/" #será la carpeta en la que se encuentra en archivo
identificadorCarp2 = "" #en caso de involucrar 2 carpetas
txt1 = "a" #en caso de involucrar un texto, se usara este, en funciones de agregar, eleminar, o reemplazar, es el texto que viene antes del agregado y/o el que hay que eliminar
txt2 = "YZ" #en caso de involucrar 2, este tambien
walk = True #Todos los archivos solo dentro de una carpeta? o dentro de sus subcarpetas tambien?
lineaAntes = False
lineaDespues = False
#esta se usa solo en archivoAaPDF y PDFaarchivo
nombres = []   #no usar variable a menos que sea estrictamente necesario
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
            crea(txt1, archivo_s[i], identificadorCarp1)
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

pdf("""
🎼 Balada de Petro: “Por qué no yo, Nobel traicionero”

Balada lenta, tono nostálgico, mezcla de ego herido y crítica geopolítica.

Estrofa 1

En la Casa de Nariño, solo y pensativo,
mira al cielo Petro, el pecho compasivo.
Un titular retumba en su corazón:
“María Corina, Nobel por la Nación”.

Estrofa 2

Se alzó la derecha, con premios y flores,
mientras él hablaba de paz y dolores.
“¿Y mi lucha por el clima, por los pobres,
no vale más que sus discursos de oradores?”

Estribillo (x2)

🎶 Ay Nobel traicionero, ¿qué fue lo que viste?
¿No viste a un hombre que al mundo resiste?
Puse el petróleo a juicio, paré el motor,
pero premias al norte y niegas mi ardor. 🎶

Estrofa 3

“¿Será que mi tono, mi verbo profundo,
no les gustó tanto en el primer mundo?
Hablo de imperios, de Wall Street y fuego…
María Corina, ¿qué hizo, sin despegar un ruego?”

Estrofa 4

Citó a Bolívar, a Marx y a Galeano,
marchó con el pueblo, alzó su mano.
“Yo soy la voz del sur global, herido,
pero me ignoran como si no hubiera nacido…”

Estribillo (x2)

🎶 Ay Nobel esquivo, juez del hemisferio,
¿acaso molesta mi tono sincero?
Premias al drama, la foto, el disfraz,
y no ves al hombre que detuvo al gas. 🎶

Cierre (con aire melancólico)

Petro suspira, con la mirada lejana:
“Quizá en otra vida, en otra mañana.
Mientras tanto, que celebren los fríos,
que yo me quedo en mis sueños vacíos…”

🎤 Batalla de rap: Aciculifolio vs Esclerófilo

Duelo botánico feroz entre dos tipos de hoja que se enfrentan en el ring vegetal.
Beat rápido, estilo freestyle, lleno de punchlines dendrológicos.

🎙️ Round 1: Aciculifolio (el pino, el elegante)

“Yo soy aguja fina, soy delgada y sutil,
soporto inviernos que a ti te hacen infantil.
Mientras tú sudas en veranos calientes,
yo conservo el agua, hojas inteligentes.

Siempre verde, siempre firme, sin caer,
tu rigidez se parte, yo puedo sostener.
Pino, abeto, conífera con flow,
te dejo seco como en clima sin snow.”

🎙️ Round 2: Esclerófilo (el roble, el duro)

“Tú pinchas suave, yo golpeo con espesor,
hoja coriácea, campeón del calor.
Mediterráneo soy, roca y sol me forjaron,
tus cloroplastos, hermano, se asustaron.

Yo sí sé de estrés hídrico y de resistencia,
mi hoja no cae con ninguna violencia.
Tú pareces duro, pero sos de cartón,
aciculifolio, aquí manda el campeón.”

🎙️ Round 3: Aciculifolio (respuesta afilada)

“Resistes calor, pero ¿y el invierno qué?
Mientras tú te secas, yo estoy de pie.
Clorofila eterna, hoja ninja ancestral,
mi estoma medita, no es superficial.

Tú eres grueso, pero eso no es virtud,
te evapora el sol con total ingratitud.
Lento pero verde, soy sabio del bosque,
tu esclerosis no asombra, ni con enfoque.”

🎙️ Round Final: Esclerófilo (remate brutal)

“Hojas duras como puño de revolución,
mi lignina golpea con precisión.
Tus acículas finas, parecen de papel,
yo doy sombra al mundo, tú apenas nivel.

Así que pinito, regresa a tu altitud,
aquí abajo se gana con actitud.
Soy roble, encina, madroño y alcornoque,
en este duelo, tú te desenfoques.”
""", "que_cosaaa", "./")
"""
# Punto de entrada del programa. Si ejecutas `python app.py`, Flask levanta el servidor local.
if __name__ == "__main__":
    # debug=True recarga el servidor al detectar cambios y muestra trazas de error legibles.
    # port=5000 hace que escuche en http://127.0.0.1:5000
    app.run(port=5000, debug=True)
"""
import os
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
    if not (isinstance(lineaAntes, bool) or isinstance(ineaDespues, bool)):
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
        before =  chueco[:ubccionmbr + len(ubicacionenArchivo)].strip()
        after = chueco[ubccionmbr + len(ubicacionenArchivo):].strip()
        
        with open(archivo, 'r+') as f:
            f.write(before + nts + txtAgregar + dsps + after)
    else:
        print("\n No exite esa parte del texto \n")

def eliminARchivo (archivo):
    if(os.path.exists(archivo)):
        os.remove(archivo)
    else:
        print("\n jaja no existeeeeee el archivo ese tuyo\n \n ")

def copiar(archivo, nuevaUbicacion):
    chueco = ""
    posicioNombre = archivo.rfind("/")
    nombre = archivo[posicioNombre + 1:].strip()
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
            if(nombres[i][posicioNombre:].strip() == terminacion):
                nombresTrmncion.append(nombres[i])
        if(nombresTrmncion == []):
            print("No se ha encontrado ningun archivo con el nombre deseado")
        return nombresTrmncion
    except FileNotFoundError:
        print("La carpeta que busca no existe")
    except ValueError:
        print(ValueError)
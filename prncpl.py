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
    with open(archivo, 'r') as e:
        chueco = e.read()
    with open(nuevaUbicacion + nombre, 'x') as f:
        f.write(chueco)

def mover(archivoM, nuevaUbicacionM):
    copiar(archivoM, nuevaUbicacionM)
    eliminARchivo(archivoM)
x = input("que texto desea agregar? ")
y = input("como se llama el archivo? ")
z = input("en que parte? donde dice que?")
modificaDondedice(x, y, z, False, False)
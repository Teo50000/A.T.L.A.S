import os
def crea(txtAgregar, archivo):
    with open(archivo, 'x') as e:
        e.write(txtAgregar)

def  modificaDondedice(txtAgregar, archivo, ubicacionenArchivo, lineaAntes, lineaDespues):
    nts = ""
    dsps = ""
    if(lineaAntes == True):
        nts = "\n"
    if(lineaDespues == True):
        dsps = "\n"
    chueco = ""
    with open(archivo, 'r') as e:
        chueco = e.read()
    ubccionmbr = chueco.find(ubicacionenArchivo)
    before =  chueco[:ubccionmbr + len(ubicacionenArchivo)].strip()
    after = chueco[ubccionmbr + len(ubicacionenArchivo):].strip()
    
    with open(archivo, 'r+') as f:
        f.write(before + nts + txtAgregar + dsps + after)

def eliminARchivo (archivo):
    if(os.path.exists(archivo)):
        os.remove(archivo)
    else:
        print("\n jaja no existeeeeee el archivo ese tuyo\n \n ")

x = input("que archivo desea elimiar? ")
eliminARchivo(x)
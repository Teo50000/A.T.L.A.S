# router.py
import re
import actions

"""
Router de ATLAS
---------------
Este módulo recibe:
 - El resultado del NLU (intención y texto original)
 - Extrae datos relevantes (slots)
 - Llama a la función correspondiente de actions.py
"""


def extract_slots(text):
    """
    Extrae elementos del texto:
     - Archivos (.txt, .pdf, etc.)
     - Carpetas (rutas o nombres)
     - Textos entre comillas ("...")
    Devuelve un diccionario con los datos detectados.
    """
    archivos = re.findall(r'\b[\w\-]+\.\w+\b', text)
    carpetas = re.findall(r'[A-Z]:\\\\[^ ]+|\/[^ ]+\/', text)
    quoted = re.findall(r'"([^"]+)"|\'([^\']+)\'', text)
    textos = [q[0] or q[1] for q in quoted]

    return {
        "archivos": archivos,
        "carpetas": carpetas,
        "textos": textos
    }



def route(intent, text):
    """
    Recibe la intención detectada (por NLU)
    y el texto original del usuario.
    Llama a la función correspondiente en actions.py.
    """
    slots = extract_slots(text)
    archivos = slots["archivos"]
    carpetas = slots["carpetas"]
    textos = slots["textos"]

    print(f"[Router] Intención detectada: {intent}")
    print(f"[Router] Archivos: {archivos}")
    print(f"[Router] Carpetas: {carpetas}")
    print(f"[Router] Textos: {textos}")

    # --- CREAR ARCHIVOS / CONVERTIR ---
    if intent == "crea":
        # Ejemplo: "crear un archivo hola.txt"
        if archivos:
            for arch in archivos:
                actions.crea(textos[0] if textos else "", arch)
        else:
            print("[Router] No se encontró nombre de archivo.")
        return

    elif intent == "archivoAaPDF":
        # Ejemplo: "convertir archivo hola.txt a pdf"
        if archivos:
            for arch in archivos:
                nombre = arch.split(".")[0]
                ruta = carpetas[0] if carpetas else "./"
                actions.archivoAaPDF(arch, nombre, ruta)
        else:
            print("[Router] No se encontró archivo para convertir.")
        return

    elif intent == "PDFaTexto":
        # Ejemplo: "convertir informe.pdf a texto"
        if archivos:
            for arch in archivos:
                nombre = arch.split(".")[0] + ".txt"
                ruta = carpetas[0] if carpetas else "./"
                actions.PDFaTexto(arch, nombre, ruta)
        else:
            print("[Router] No se encontró PDF para convertir.")
        return

    elif intent == "modificaDondeDice":
        if len(textos) >= 2 and archivos:
            actions.modificaDondeDice(textos[0], archivos[0], textos[1], False, False)
        else:
            print("[Router] Faltan parámetros para modificar.")
        return

    elif intent == "reemplazar":
        if len(textos) >= 2 and archivos:
            actions.reemplazar(textos[0], archivos[0], textos[1])
        else:
            print("[Router] Faltan parámetros para reemplazar.")
        return

    elif intent == "sacarLoQueDice":
        if textos and archivos:
            actions.sacarLoQueDice(archivos[0], textos[0])
        else:
            print("[Router] Faltan datos para eliminar texto.")
        return

    elif intent == "eliminARchivo":
        if archivos:
            for arch in archivos:
                actions.eliminARchivo(arch)
        else:
            print("[Router] No se encontró archivo a eliminar.")
        return

    elif intent == "copiar":
        if archivos and carpetas:
            for arch in archivos:
                actions.copiar(arch, carpetas[0])
        else:
            print("[Router] Faltan ruta o archivo para copiar.")
        return

    elif intent == "mover":
        if archivos and carpetas:
            for arch in archivos:
                actions.mover(arch, carpetas[0])
        else:
            print("[Router] Faltan ruta o archivo para mover.")
        return

    elif intent == "renombrar":
        if len(archivos) >= 1 and textos:
            actions.renombrar(archivos[0], textos[0])
        else:
            print("[Router] Faltan parámetros para renombrar.")
        return

    elif intent == "dupdic":
        if len(carpetas) >= 2:
            actions.dupdic(carpetas[0], carpetas[1])
        else:
            print("[Router] Faltan carpetas para duplicar.")
        return

    elif intent == "movdic":
        if len(carpetas) >= 2:
            actions.movdic(carpetas[0], carpetas[1])
        else:
            print("[Router] Faltan carpetas para mover.")
        return

    else:
        print(f"[Router] Intención desconocida o no implementada: {intent}")
        return

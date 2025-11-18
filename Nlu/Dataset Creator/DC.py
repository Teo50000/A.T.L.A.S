# DC.py — generador de dataset completo para ATLAS
import csv
import random
import unicodedata
from pathlib import Path

# =========================================================
# 🧩 Definición de intenciones
# =========================================================
INTENTS = {
    # Crear archivos
    "crea": {
        "templates": [
            "{inicio} {verbo} un archivo llamado {nombre}",
            "{inicio} quiero {verbo} {nombre}",
            "{inicio} haceme {verbo} {nombre}",
            "{inicio} necesito {verbo} un nuevo archivo {nombre}",
            "{inicio} podés {verbo} un archivo {nombre}",
            "{inicio} creá {nombre}",
            "{inicio} generá el archivo {nombre}"
        ],
        "sinonimos_verbo": ["crear", "generar", "armar", "hacer", "producir", "escribir"],
        "nombres": ["notas.txt", "reporte.docx", "nuevo.txt", "diario.txt"]
    },

    # Convertir texto a PDF
    "archivoAaPDF": {
        "templates": [
            "{inicio} {verbo} {archivo} a PDF",
            "{inicio} pasá {archivo} a pdf",
            "{inicio} convertí {archivo} en formato pdf",
            "{inicio} transformá {archivo} en un pdf",
            "{inicio} hacé un pdf con {archivo}"
        ],
        "sinonimos_verbo": ["convertir", "pasar", "transformar", "guardar", "cambiar"],
        "archivo": ["informe.txt", "reporte.txt", "notas.txt", "texto.txt"]
    },

    # Convertir PDF a texto
    "PDFaTexto": {
        "templates": [
            "{inicio} {verbo} {archivo} a texto",
            "{inicio} pasá {archivo} a txt",
            "{inicio} extraé el texto de {archivo}",
            "{inicio} convertí {archivo} en texto plano",
            "{inicio} hacé texto de {archivo}"
        ],
        "sinonimos_verbo": ["convertir", "extraer", "pasar", "transformar", "sacar"],
        "archivo": ["informe.pdf", "documento.pdf", "reporte.pdf"]
    },

    # Modificar donde dice
    "modificaDondeDice": {
        "templates": [
            "{inicio} agregá {nuevo} donde diga {antiguo} en {archivo}",
            "{inicio} insertá {nuevo} antes de {antiguo} en {archivo}",
            "{inicio} escribí {nuevo} después de {antiguo} en {archivo}",
            "{inicio} poné {nuevo} donde dice {antiguo} dentro de {archivo}"
        ],
        "sinonimos_verbo": ["agregar", "escribir", "insertar", "añadir", "poner"],
        "archivo": ["notas.txt", "reporte.txt", "plan.txt"],
        "antiguo": ["hola", "resumen", "dato", "total"],
        "nuevo": ["adiós", "nuevo resumen", "información actualizada", "cálculo"]
    },

    # Reemplazar texto
    "reemplazar": {
        "templates": [
            "{inicio} reemplazá {antiguo} por {nuevo} en {archivo}",
            "{inicio} cambiá {antiguo} por {nuevo} dentro de {archivo}",
            "{inicio} sustituí {antiguo} con {nuevo} en {archivo}",
            "{inicio} cambiá la palabra {antiguo} por {nuevo} en {archivo}"
        ],
        "sinonimos_verbo": ["reemplazar", "cambiar", "sustituir"],
        "archivo": ["notas.txt", "reporte.txt", "plan.txt"],
        "antiguo": ["hola", "dato", "resumen", "mundo"],
        "nuevo": ["chau", "nuevo dato", "nuevo resumen", "planeta"]
    },

    # Sacar texto
    "sacarLoQueDice": {
        "templates": [
            "{inicio} borrá lo que diga {antiguo} en {archivo}",
            "{inicio} eliminá la palabra {antiguo} de {archivo}",
            "{inicio} quitá {antiguo} del archivo {archivo}",
            "{inicio} sacá todo lo que diga {antiguo} en {archivo}"
        ],
        "sinonimos_verbo": ["borrar", "eliminar", "quitar", "sacar"],
        "archivo": ["notas.txt", "reporte.txt", "plan.txt"],
        "antiguo": ["hola", "dato", "resumen", "total"]
    },

    # Eliminar archivos
    "eliminARchivo": {
        "templates": [
            "{inicio} {verbo} el archivo {nombre}",
            "{inicio} {verbo} {nombre}",
            "{inicio} quiero {verbo} {nombre}",
            "{inicio} sacá {nombre}",
            "{inicio} borrá {nombre} que ya no sirve"
        ],
        "sinonimos_verbo": ["borrar", "eliminar", "sacar", "quitar", "remover"],
        "nombres": ["viejo.txt", "reporte.docx", "basura.pdf", "log.txt"]
    },

    # Copiar archivos
    "copiar": {
        "templates": [
            "{inicio} {verbo} {archivo} a {destino}",
            "{inicio} hacé una copia de {archivo} en {destino}",
            "{inicio} duplicá {archivo} dentro de {destino}",
            "{inicio} pasá {archivo} a {destino}"
        ],
        "sinonimos_verbo": ["copiar", "duplicar", "respaldar", "clonar"],
        "archivo": ["informe.docx", "plan.txt", "datos.csv"],
        "destino": ["docs/", "backup/", "seguridad/"]
    },

    # Mover archivos
    "mover": {
        "templates": [
            "{inicio} {verbo} {archivo} a {destino}",
            "{inicio} trasladá {archivo} hacia {destino}",
            "{inicio} mové {archivo} al directorio {destino}",
            "{inicio} pasá {archivo} dentro de {destino}"
        ],
        "sinonimos_verbo": ["mover", "trasladar", "reubicar"],
        "archivo": ["notas.txt", "reporte.docx", "plan.txt"],
        "destino": ["proyectos/", "backup/", "docs/"]
    },

    # Renombrar archivos
    "renombrar": {
        "templates": [
            "{inicio} renombrá {archivo} a {nuevo}",
            "{inicio} renombrar {archivo} por {nuevo}",
            "{inicio} cambiá el nombre de {archivo} a {nuevo}",
            "{inicio} ponéle {nuevo} a {archivo}",
            "{inicio} dejá {archivo} con el nombre {nuevo}"
        ],
        "sinonimos_verbo": ["renombrar", "cambiar nombre", "ponerle"],
        "archivo": ["notas.txt", "reporte.docx", "plan.txt", "datos.csv"],
        "nuevo": ["notas_nuevo.txt", "reporte_final.docx", "plan_2025.txt", "dataset.csv"]
    },

    # Duplicar carpetas
    "dupdic": {
        "templates": [
            "{inicio} {verbo} la carpeta {carvieja} en {carnueva}",
            "{inicio} hacé una copia de {carvieja} dentro de {carnueva}",
            "{inicio} duplicá {carvieja} a {carnueva}"
        ],
        "sinonimos_verbo": ["duplicar", "copiar", "respaldar", "clonar"],
        "carvieja": ["proyectos/", "imagenes/", "reportes/"],
        "carnueva": ["backup/", "archivos/", "respaldo/"]
    },

    # Mover carpetas
    "movdic": {
        "templates": [
            "{inicio} {verbo} la carpeta {carvieja} a {carnueva}",
            "{inicio} trasladá {carvieja} hacia {carnueva}",
            "{inicio} mové {carvieja} dentro de {carnueva}"
        ],
        "sinonimos_verbo": ["mover", "trasladar", "reubicar"],
        "carvieja": ["proyectos/", "imagenes/", "reportes/"],
        "carnueva": ["backup/", "archivos/", "respaldo/"]
    },

    # Leer archivo
    "leerArchivo": {
        "templates": [
            "{inicio} {verbo} el archivo {archivo}",
            "{inicio} {verbo} {archivo}",
            "{inicio} mostrame el contenido de {archivo}",
            "{inicio} abrí {archivo}",
            "{inicio} quiero leer {archivo}"
        ],
        "sinonimos_verbo": ["leer", "mostrar", "ver", "abrir", "consultar"],
        "archivo": ["notas.txt", "informe.txt", "reporte.txt"]
    },

    # Buscar archivo por nombre
    "buscarArchivo": {
        "templates": [
            "{inicio} {verbo} el archivo llamado {archivo}",
            "{inicio} {verbo} {archivo} en todo el disco",
            "{inicio} encontrá el archivo {archivo}",
            "{inicio} localizá {archivo}"
        ],
        "sinonimos_verbo": ["buscar", "encontrar", "localizar", "verificar"],
        "archivo": ["informe.txt", "plan.pdf", "reporte.docx"]
    },

    # Buscar carpeta por nombre
    "buscarCarpeta": {
        "templates": [
            "{inicio} {verbo} la carpeta {carpeta}",
            "{inicio} {verbo} {carpeta} en todo el disco",
            "{inicio} localizá la carpeta {carpeta}",
            "{inicio} encontrá {carpeta}"
        ],
        "sinonimos_verbo": ["buscar", "encontrar", "localizar"],
        "carpeta": ["proyectos", "imagenes", "documentos"]
    },

    # Listar archivos de un tipo en una carpeta
    "listarTipo": {
        "templates": [
            "{inicio} {verbo} todos los archivos {tipo} en {carpeta}",
            "{inicio} listá los archivos {tipo} dentro de {carpeta}",
            "{inicio} mostrame los {tipo} que haya en {carpeta}"
        ],
        "sinonimos_verbo": ["listar", "buscar", "mostrar", "ver"],
        "tipo": [".txt", ".pdf", ".csv"],
        "carpeta": ["proyectos/", "docs/", "backup/"]
    },

    # Leer texto de un PDF
    "leerPDF": {
        "templates": [
            "{inicio} {verbo} el contenido de {archivo}",
            "{inicio} extraé el texto de {archivo}",
            "{inicio} mostrame lo que dice {archivo}"
        ],
        "sinonimos_verbo": ["leer", "mostrar", "extraer", "ver"],
        "archivo": ["informe.pdf", "reporte.pdf", "documento.pdf"]
    }
}


# =========================================================
# ⚙️ Auxiliares
# =========================================================
INICIOS = [
    "", "por favor", "quiero", "necesito", "podés", "che", "eh", "dale",
    "haceme el favor de", "cuando puedas", "porfa", "sería bueno si"
]

ERRORES_COMUNES = {
    "pdf": ["pfd", "pdff"],
    "archivo": ["archibo", "archvo"],
    "texto": ["texo", "teto"],
    "crear": ["crar", "cerar"],
    "mover": ["mobver", "mober"],
    "eliminar": ["elimnar", "elminar"]
}


def introducir_errores(frase):
    for palabra, errores in ERRORES_COMUNES.items():
        if palabra in frase and random.random() < 0.1:
            frase = frase.replace(palabra, random.choice(errores))
    return frase


def normalizar(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )


# =========================================================
# 🧠 Generador principal
# =========================================================
def generar_dataset(intents=INTENTS, archivo_salida="data/intents.csv", ejemplos_por_intent=500):
    filas = []

    for intent, info in intents.items():
        templates = info["templates"]

        for _ in range(ejemplos_por_intent):
            t = random.choice(templates)
            frase = t.format(
                inicio=random.choice(INICIOS),
                verbo=random.choice(info.get("sinonimos_verbo", ["hacer"])),
                nombre=random.choice(info.get("nombres", ["archivo.txt"])),
                archivo=random.choice(info.get("archivo", ["archivo.txt"])),
                destino=random.choice(info.get("destino", ["./"])),
                carvieja=random.choice(info.get("carvieja", ["carpeta/"])),
                carnueva=random.choice(info.get("carnueva", ["respaldo/"])),
                antiguo=random.choice(info.get("antiguo", ["viejo"])),
                nuevo=random.choice(info.get("nuevo", ["nuevo"])),
                carpeta=random.choice(info.get("carpeta", ["docs"])),
                tipo=random.choice(info.get("tipo", [".txt"]))
            ).strip()

            if random.random() < 0.05:
                frase = frase.upper()
            if random.random() < 0.03:
                frase = frase.replace(" ", "  ")

            frase = introducir_errores(frase)
            frase = normalizar(frase)

            filas.append((frase, intent))

    random.shuffle(filas)
    Path("data").mkdir(exist_ok=True)
    with open(archivo_salida, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "intent"])
        writer.writerows(filas)

    print(f"[✓] Dataset generado: {archivo_salida} ({len(filas)} ejemplos totales)")


if __name__ == "__main__":
    generar_dataset(INTENTS, ejemplos_por_intent=500)

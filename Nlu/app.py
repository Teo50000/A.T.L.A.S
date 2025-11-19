import os
from nlu import predict
from router import route

"""
ATLAS — Sistema central de ejecución
------------------------------------
app.py es el punto de entrada del sistema:
 - Recibe texto (manual o por voz)
 - Usa el NLU para entender la intención
 - Usa el router para decidir qué hacer
 - Ejecuta la acción correspondiente (en actions.py)
"""

def banner():
    print("""
  ======================================
            A . T . L . A . S
  ======================================
  Escribí una orden como:
    - crear un archivo notas.txt
    - pasar texto a pdf
    - convertir informe.pdf a texto
    - borrar documento viejo.txt
  --------------------------------------
    'exit' para salir
  ======================================
    """)


def main():
    os.system("cls" if os.name == "nt" else "clear")
    banner()

    while True:
        # Leer orden del usuario
        user_input = input("\nIngresá tu comando: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ["exit", "salir", "quit"]:
            print("\n Cerrando ATLAS...")
            break

        # interpretar intención
        print("\nAnalizando intención...")
        result = predict(user_input)
        intent = result.get("intent")
        confidence = result.get("confidence")

        print(f"Intención: {intent} (confianza: {confidence*100:.1f}%)")

        # ejecutar acción mediante router
        print("\nEjecutando acción...\n")
        route(intent, user_input)

        print("\n--------------------------------------")


if __name__ == "__main__":
    main()

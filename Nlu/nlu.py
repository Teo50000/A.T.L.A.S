import os
import re
import joblib
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

#avenida libertador
MODEL_PATH = os.path.join("models", "intent_clf.pkl")
DATA_PATH = os.path.join("data", "intents.csv")


#stopwoerds
# Usamos stopwords en español y las combinamos con las de sklearn
spanish_stopwords = list(text.ENGLISH_STOP_WORDS.union({
    "de", "la", "que", "el", "en", "y", "a", "los", "del", "se", "las",
    "por", "un", "para", "con", "no", "una", "su", "al", "lo", "como",
    "más", "pero", "sus", "le", "ya", "o", "fue", "ha", "sí", "porque",
    "esta", "son", "entre", "cuando", "muy", "sin", "sobre", "también",
    "me", "hasta", "hay", "donde", "quien", "desde", "todo", "nos",
    "durante", "todos", "uno", "les", "ni", "contra", "otros", "ese",
    "eso", "ante", "ellos", "e", "esto", "mí", "antes", "algunos",
    "qué", "unos", "yo", "otro", "otras", "otra", "él", "quiero",
    "porfa", "hacer", "crear", "pasar", "convertir", "archivo"
}))


#entrenar
def train():
    """Entrena el modelo de comprensión de lenguaje y lo guarda en /models/intent_clf.pkl"""
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"No se encontró el dataset: {DATA_PATH}")

    # Cargar dataset
    data = pd.read_csv(DATA_PATH)
    X = data["text"]
    y = data["intent"]

    # Dividir dataset en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # victoooooooooooooor,victoooooooooooooor, y regresin logistica
    clf = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 2),
            lowercase=True,
            stop_words=spanish_stopwords,
            strip_accents='unicode'
        )),
        ("lr", LogisticRegression(max_iter=30000, class_weight='balanced'))
    ])

    # Entrenar modelo
    clf.fit(X_train, y_train)

    # Evaluar modelo
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"[✓] Accuracy de validación: {acc*100:.2f}% ({len(X_test)} ejemplos)")

    # Guardar modelo entrenado
    os.makedirs("models", exist_ok=True)
    joblib.dump(clf, MODEL_PATH)
    print(f"[💾] Modelo entrenado y guardado en {MODEL_PATH}")

    #Hacer que el modelo me rasque las pelotas a este punto


#predict de beniju
def load_model():
    """Carga el modelo entrenado desde /models/"""
    if not os.path.exists(MODEL_PATH):
        print("[!] Modelo no encontrado, entrenando uno nuevo...")
        train()
    return joblib.load(MODEL_PATH)


def predict(text: str):
    """Predice la intención y aplica correcciones semánticas simples"""
    model = load_model()
    text_lower = text.lower()
    intent = model.predict([text])[0]
    proba = model.predict_proba([text])[0].max()

    # Reglas semanticas inteligentes
    # Si no se menciona PDF, no puede ser una conversión a PDF
    if "pdf" not in text_lower and "convert" not in text_lower and intent == "archivoAaPDF":
        intent = "crea"

    # Si el usuario dice “convertir” y “pdf”, forzamos a archivoAaPDF
    if any(w in text_lower for w in ["convertir", "pasar", "transformar"]) and "pdf" in text_lower:
        intent = "archivoAaPDF"

    # Si el texto incluye “texto” y un .pdf, probablemente quiere PDFaTexto
    if "texto" in text_lower and ".pdf" in text_lower:
        intent = "PDFaTexto"

    # Si menciona “borrar”, “eliminar”, “quitar”, reforzamos esa intención
    if any(w in text_lower for w in ["borrar", "eliminar", "quitar", "remover"]) and ".pdf" not in text_lower:
        intent = "eliminARchivo"

    # Si menciona “mover” o “trasladar” + carpeta, reforzamos mover
    if any(w in text_lower for w in ["mover", "trasladar", "reubicar"]) and "/" in text_lower:
        intent = "mover"

    # ⚠️ Protección: si la confianza es muy baja, no ejecutar nada
    if proba < 0.45:
        print("⚠️ Confianza baja. No se ejecutará ninguna acción automática.")
        intent = "desconocido"

    # Slots simples
    archivos = re.findall(r'\b[\w\-]+\.\w+\b', text)
    carpetas = re.findall(r'([A-Za-z]:\\[^ ]+|\/[^ ]+\/)', text)

    return {
        "intent": intent,
        "confidence": round(float(proba), 2),
        "archivos": archivos,
        "carpetas": carpetas
    }





if __name__ == "__main__":
    print("Entrenando y probando el modelo NLU...\n")
    train()
    print("\nEjemplo de predicción:")
    print(predict("quiero convertir el informe.pdf a texto"))

import os
import psycopg2
from flask import Flask, render_template, request
import google.generativeai as genai
from dotenv import load_dotenv

# ==========================================================
# CHARGEMENT DES VARIABLES D'ENVIRONNEMENT
# ==========================================================
load_dotenv()

app = Flask(__name__)

# ==========================================================
# CONFIG GEMINI
# ==========================================================
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel("models/gemini-flash-lite-latest")

# ==========================================================
# CONFIG POSTGRESQL
# ==========================================================
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
   
}


def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)


def get_infos_universite():
    """Récupère toutes les infos de la table pour servir de contexte au LLM."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT question, reponse FROM infos_universite;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def construire_contexte(rows):
    contexte = ""
    for question, reponse in rows:
        contexte += f"Q: {question}\nR: {reponse}\n\n"
    return contexte

def generer_reponse(question_utilisateur):
    print("ETAPE 1 : entrée dans generer_reponse")

    try:
        print("ETAPE 1.1 : tentative connexion PostgreSQL")
        conn = get_db_connection()
        print("ETAPE 1.2 : connexion PostgreSQL OK")

        cur = conn.cursor()
        print("ETAPE 1.3 : curseur créé")

        cur.execute("SELECT question, reponse FROM infos_universite;")
        print("ETAPE 1.4 : requête SQL exécutée")

        rows = cur.fetchall()
        print("ETAPE 1.5 : données récupérées")
        print(rows)

        cur.close()
        conn.close()

        contexte = construire_contexte(rows)
        print("ETAPE 2 : contexte construit")

        prompt = f"""Tu es un assistant de l'Université Virtuelle du Burkina.

Informations disponibles :
{contexte}

Question :
{question_utilisateur}

Réponds en français de manière claire et concise.
"""

        print("ETAPE 3 : appel Gemini")

        response = gemini_model.generate_content(prompt)

        print("ETAPE 4 : réponse Gemini reçue")

        return response.text

    except Exception as e:
        print("========== ERREUR ==========")
        print(type(e))
        print(repr(e))
        print("============================")
        raise

@app.route("/", methods=["GET", "POST"])
def index():
    reponse = None
    question = None

    if request.method == "POST":
        question = request.form.get("question", "").strip()
        if question:
            try:
                reponse = generer_reponse(question)
            except Exception as e:
                reponse = f"Une erreur est survenue lors de la génération de la réponse : {e}"

    return render_template("index.html", question=question, reponse=reponse)


if __name__ == "__main__":
    app.run(debug=True)
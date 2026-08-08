"""
Script pour (re)créer la table et insérer les données proprement,
en évitant les problèmes d'encodage liés au terminal Windows (cmd/psql).
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "client_encoding": "utf8"
    
}

DONNEES = [
    (
        "Qu'est-ce que l'Université Virtuelle du Burkina ?",
        "L'Université Virtuelle du Burkina (UVB) est un établissement public d'enseignement "
        "supérieur au Burkina Faso, spécialisé dans la formation à distance et l'utilisation "
        "des technologies numériques pour l'apprentissage.",
    ),
    (
        "Quelles filières propose l'UVB ?",
        "L'UVB propose plusieurs filières, notamment en Informatique, Génie Logiciel et "
        "Communication Digitale, selon les années académiques et l'évolution de l'offre de formation.",
    ),
    (
        "Comment s'inscrire à l'UVB ?",
        "L'inscription à l'UVB se fait généralement en ligne via la plateforme officielle de "
        "l'université, après le baccalauréat ou selon les conditions d'admission en vigueur.",
    ),
    (
        "Où se trouve l'UVB ?",
        "L'UVB est basée à Ouagadougou, avec des centres d'accès au numérique (CAN) répartis "
        "dans plusieurs régions du Burkina Faso pour permettre aux étudiants d'accéder aux cours.",
    ),
    (
        "L'UVB délivre-t-elle des diplômes reconnus ?",
        "Oui, l'UVB délivre des diplômes reconnus par l'État burkinabè, au même titre que les "
        "autres universités publiques du pays.",
    ),
    (
        "Les cours à l'UVB sont-ils entièrement en ligne ?",
        "Oui, les enseignements à l'UVB sont dispensés principalement à distance via une "
        "plateforme numérique, avec parfois des regroupements ou évaluations en présentiel "
        "dans les centres d'accès au numérique.",
    ),
]


def main():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Crée la table si elle n'existe pas encore
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS infos_universite (
            id SERIAL PRIMARY KEY,
            question TEXT NOT NULL,
            reponse TEXT NOT NULL
        );
        """
    )

    # Vide la table pour repartir sur des données propres
    cur.execute("TRUNCATE TABLE infos_universite RESTART IDENTITY;")

    # Insère les données via des paramètres (psycopg2 gère l'UTF-8 correctement)
    cur.executemany(
        "INSERT INTO infos_universite (question, reponse) VALUES (%s, %s);",
        DONNEES,
    )

    conn.commit()
    cur.close()
    conn.close()
    print(f"{len(DONNEES)} lignes insérées avec succès en UTF-8.")


if __name__ == "__main__":
    main()
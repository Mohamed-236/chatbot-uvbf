-- Active: 1786099674743@@127.0.0.1@5432@uvbf_chatbot@public
-- ==========================================================
-- Schéma de la base de données pour le chatbot UVB
-- ==========================================================

CREATE DATABASE IF NOT EXISTS uvb_chatbot;


CREATE TABLE IF NOT EXISTS infos_universite (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    reponse TEXT NOT NULL
);

-- ==========================================================
-- Quelques données d'exemple (à adapter avec les vraies infos de l'UVB)
-- ==========================================================

INSERT INTO infos_universite (question, reponse) VALUES
('Qu''est-ce que l''Université Virtuelle du Burkina ?',
 'L''Université Virtuelle du Burkina (UVB) est un établissement public d''enseignement supérieur au Burkina Faso, spécialisé dans la formation à distance et l''utilisation des technologies numériques pour l''apprentissage.'),

('Quelles filières propose l''UVB ?',
 'L''UVB propose plusieurs filières, notamment en Informatique, Génie Logiciel et Communication Digitale, selon les années académiques et l''évolution de l''offre de formation.'),

('Comment s''inscrire à l''UVB ?',
 'L''inscription à l''UVB se fait généralement en ligne via la plateforme officielle de l''université, après le baccalauréat ou selon les conditions d''admission en vigueur.'),

('Où se trouve l''UVB ?',
 'L''UVB est basée à Ouagadougou, avec des centres d''accès au numérique (CAN) répartis dans plusieurs régions du Burkina Faso pour permettre aux étudiants d''accéder aux cours.'),

('L''UVB délivre-t-elle des diplômes reconnus ?',
 'Oui, l''UVB délivre des diplômes reconnus par l''État burkinabè, au même titre que les autres universités publiques du pays.'),

('Les cours à l''UVB sont-ils entièrement en ligne ?',
 'Oui, les enseignements à l''UVB sont dispensés principalement à distance via une plateforme numérique, avec parfois des regroupements ou évaluations en présentiel dans les centres d''accès au numérique.');


SELECT * FROM infos_universite;
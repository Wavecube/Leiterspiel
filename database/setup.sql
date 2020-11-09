CREATE DATABASE IF NOT EXISTS highscores;

USE highscores;

CREATE TABLE spieler(
    spieler_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE highscore_liste(
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    spieler_id INT NOT NULL,
    highscore INT NOT NULL,
    FOREIGN KEY (spieler_id) REFERENCES spieler(spieler_id)
);
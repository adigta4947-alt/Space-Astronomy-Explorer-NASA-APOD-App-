CREATE DATABASE IF NOT EXISTS spaceapp;
USE spaceapp;

CREATE TABLE IF NOT EXISTS apod (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    date        VARCHAR(20) UNIQUE,
    title       TEXT,
    explanation LONGTEXT,
    url         TEXT,
    media_type  VARCHAR(20),
    fetched_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS favourites (
    id        INT AUTO_INCREMENT PRIMARY KEY,
    apod_id   INT,
    saved_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (apod_id) REFERENCES apod(id)
);

CREATE TABLE IF NOT EXISTS search_log (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    keyword     VARCHAR(255),
    searched_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE DATABASE spaceapp;
USE spaceapp;
SHOW TABLES;
USE spaceapp;
SELECT date, title, url, media_type FROM apod WHERE media_type != 'image';
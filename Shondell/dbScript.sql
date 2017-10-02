CREATE DATABASE Dermagram;
USE Dermagram;

CREATE TABLE DG_User(username VARCHAR(50) NOT NULL, password  VARCHAR(50), email  VARCHAR(50), firstName  VARCHAR(50), lastName VARCHAR(50), sex CHAR(1), age INT, location VARCHAR(50),  PRIMARY KEY(username));

CREATE TABLE Image(link VARCHAR(200), username_fk VARCHAR(50), FOREIGN KEY(username_fk) REFERENCES DG_User(username));





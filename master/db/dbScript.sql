CREATE DATABASE Dermagram;
USE Dermagram;

CREATE TABLE DG_User(username VARCHAR(50) NOT NULL, password  VARCHAR(500), email  VARCHAR(50), firstName  VARCHAR(50)
, lastName VARCHAR(50), albumLink VARCHAR(200),  PRIMARY KEY(username));




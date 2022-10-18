-- Local database definition.

DROP DATABASE IF EXISTS emotions_db;

CREATE DATABASE emotions_db;

USE emotions_db;

DROP TABLE IF EXISTS emotions_analysis;

CREATE TABLE emotions_analysis (
  id int NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL DEFAULT '',
  emotion VARCHAR(255) NOT NULL DEFAULT 'undetermined',
  date VARCHAR(255),
  PRIMARY KEY (id)
);
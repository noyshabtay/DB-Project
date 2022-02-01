CREATE TABLE titles
(
film_id MEDIUMINT UNSIGNED NOT NULL PRIMARY KEY,
title VARCHAR(86) NOT NULL
);

CREATE TABLE people
(
	person_id SMALLINT UNSIGNED NOT NULL PRIMARY KEY,
	name VARCHAR(32)
);

CREATE TABLE wiki
(
film_id MEDIUMINT UNSIGNED NOT NULL PRIMARY KEY,
FOREIGN KEY(film_id) REFERENCES titles(film_id),
url VARCHAR(116)
);

CREATE TABLE writers
(
	film_id MEDIUMINT UNSIGNED NOT NULL,
	writer_id SMALLINT UNSIGNED NOT NULL,
	FOREIGN KEY(film_id) REFERENCES titles(film_id),
	FOREIGN KEY(writer_id) REFERENCES people(person_id),
	PRIMARY KEY(film_id,writer_id)
);

CREATE TABLE actors 
(
	film_id MEDIUMINT UNSIGNED NOT NULL,
	actor_id SMALLINT UNSIGNED NOT NULL,
	FOREIGN KEY(film_id) REFERENCES titles(film_id),
	FOREIGN KEY(actor_id) REFERENCES people(person_id),
	PRIMARY KEY(film_id,actor_id)
);

CREATE TABLE boxOffice
(
film_id MEDIUMINT UNSIGNED NOT NULL PRIMARY KEY,
FOREIGN KEY(film_id) REFERENCES titles(film_id),
revenue INT UNSIGNED
);

CREATE TABLE directors 
(
	film_id MEDIUMINT UNSIGNED NOT NULL,
	director_id SMALLINT UNSIGNED NOT NULL,
	FOREIGN KEY(film_id) REFERENCES titles(film_id),
	FOREIGN KEY(director_id) REFERENCES people(person_id),
	PRIMARY KEY(film_id,director_id)
);

CREATE TABLE genres
(
film_id MEDIUMINT UNSIGNED NOT NULL,
FOREIGN KEY(film_id) REFERENCES titles(film_id),
genre VARCHAR(11),
PRIMARY KEY(film_id, genre)
);

CREATE TABLE imdb
(
film_id MEDIUMINT UNSIGNED NOT NULL PRIMARY KEY,
FOREIGN KEY(film_id) REFERENCES titles(film_id),
score DECIMAL(3,1)
);

CREATE TABLE plot
(
film_id MEDIUMINT UNSIGNED NOT NULL PRIMARY KEY,
FOREIGN KEY(film_id) REFERENCES titles(film_id),
description VARCHAR(400)
);
Alter table plot ADD FULLTEXT (description);

CREATE TABLE runtime 
(
	film_id MEDIUMINT UNSIGNED NOT NULL PRIMARY KEY,
	FOREIGN KEY(film_id) REFERENCES titles(film_id),
	lengthInMinutes TINYINT UNSIGNED
);
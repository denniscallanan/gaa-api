
/* RESET SCHEMA */

DROP TABLE team;


/* TEAM TABLE */

CREATE TABLE team (
	team_id serial PRIMARY KEY,
	team_name VARCHAR ( 50 ) NOT NULL,
    sport VARCHAR (12),
	est_year SMALLINT,
    is_county BOOLEAN NOT NULL DEFAULT true
);


/* TEST DATA */

INSERT INTO team (team_name, sport, est_year) VALUES ('Carlow', 'Hurling', 1930);
INSERT INTO team (team_name, sport, is_county) VALUES ('Kerry', 'Football', false);
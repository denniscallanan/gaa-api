
/* RESET SCHEMA */

DROP TABLE IF EXISTS match;
DROP TABLE IF EXISTS player;
DROP TABLE IF EXISTS team_manager;
DROP TABLE IF EXISTS team;
DROP TABLE IF EXISTS referee;
DROP TABLE IF EXISTS venue;
DROP TABLE IF EXISTS championship;


/* TEAM TABLE */


CREATE TABLE championship (
    championship_id serial PRIMARY KEY,
	championship_name VARCHAR (100) NOT NULL,
	descript VARCHAR (1000)
);


CREATE TABLE venue (
	venue_id serial PRIMARY KEY,
	venue_name VARCHAR ( 50 ) NOT NULL,
    venue_county VARCHAR ( 50 ),
	year_built INTEGER
);

CREATE TABLE referee (
    referee_id serial PRIMARY KEY,
	full_name VARCHAR (100) NOT NULL,
	dob DATE,
    career_start DATE,
	career_end DATE,
    county VARCHAR ( 50 )
);

CREATE TABLE team (
	team_id serial PRIMARY KEY,
	team_name VARCHAR ( 50 ) NOT NULL,
    sport VARCHAR (12),
	est_year SMALLINT,
    is_county BOOLEAN NOT NULL DEFAULT true,
    main_venue_id INTEGER REFERENCES venue(venue_id)
);

CREATE TABLE team_manager (
    team_manager_id serial PRIMARY KEY,
	full_name VARCHAR (100) NOT NULL,
	dob DATE,
    position_start DATE,
	position_end DATE,
	team_id INTEGER REFERENCES team(team_id)
);

CREATE TABLE player (
    player_id serial PRIMARY KEY,
	full_name VARCHAR (100) NOT NULL,
	dob DATE,
    career_start DATE,
	career_end DATE,
    typical_position VARCHAR (30),
    team_id INTEGER REFERENCES team(team_id),
    caps INTEGER
);

CREATE TABLE match (
	match_id serial PRIMARY KEY,
	home_team_id INTEGER REFERENCES team(team_id) NOT NULL,
    away_team_id INTEGER REFERENCES team(team_id) NOT NULL,
    home_team_manager_id INTEGER REFERENCES team_manager(team_manager_id),
    away_team_manager_id INTEGER REFERENCES team_manager(team_manager_id),
    home_team_goals INTEGER NOT NULL,
    home_team_points INTEGER NOT NULL,
    away_team_goals INTEGER NOT NULL,
    away_team_points INTEGER NOT NULL,
    match_date DATE,
    match_time TIME,
    championship_id INTEGER REFERENCES championship(championship_id),
    championship_round VARCHAR (5),
    is_replay BOOLEAN NOT NULL DEFAULT false,
    venue_id INTEGER REFERENCES venue(venue_id),
    half_time BOOLEAN,
    full_time BOOLEAN,
    extra_time BOOLEAN,
    referee_id INTEGER REFERENCES referee(referee_id)
);



/* TEST DATA */

INSERT INTO championship (championship_name, descript) VALUES ('All-Ireland Hurling Championship', 'The top tier national championship');
INSERT INTO venue (venue_name, venue_county, year_built) VALUES ('Croke Park', 'Dublin', 1880);
INSERT INTO venue (venue_name, venue_county, year_built) VALUES ('Dr Cullen Park', 'Carlow', 1936);
INSERT INTO referee (full_name, dob, county) VALUES ('Frank Murphy', '1944-01-05', 'Cork');
INSERT INTO team (team_name, sport, est_year, is_county, main_venue_id) VALUES ('Carlow', 'Hurling', 1930, true, 2);
INSERT INTO team (team_name, sport, est_year, is_county, main_venue_id) VALUES ('Dublin', 'Hurling', 1898, true, 1);
INSERT INTO team (team_name, sport, est_year, is_county, main_venue_id) VALUES ('BallyBoden St Endas', 'Hurling', 1966, false, 1);
INSERT INTO player (full_name, dob, team_id, caps) VALUES ('DJ Carey', '1974-01-05', 1, 100);
INSERT INTO team_manager (full_name, dob, position_start, team_id) VALUES ('Davy Fitzgerald', '1974-07-05', '2014-07-05', 1);
INSERT INTO match 
    (home_team_id, away_team_id, home_team_goals, home_team_points, away_team_goals, 
    away_team_points, match_date, championship_id, championship_round, is_replay, 
    venue_id, half_time, full_time, extra_time, referee_id) 
    VALUES (1, 2, 1, 22, 3, 20, '2020-05-05', 1, 'F', false, 1, true, true, true, 1);

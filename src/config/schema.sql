
/* RESET SCHEMA */

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


DROP TABLE IF EXISTS match;
DROP TABLE IF EXISTS player;
DROP TABLE IF EXISTS team_manager;
DROP TABLE IF EXISTS team;
DROP TABLE IF EXISTS referee;
DROP TABLE IF EXISTS venue;
DROP TABLE IF EXISTS championship;
DROP TABLE IF EXISTS portal_user;


/* TEAM TABLE */


CREATE TABLE portal_user (
    id_tag serial PRIMARY KEY,
    google_sub VARCHAR (50),
	reported_count SMALLINT NOT NULL DEFAULT 0
);

CREATE TABLE championship (
	id_tag VARCHAR (50) NOT NULL,
	championship_name VARCHAR (100) NOT NULL,
	descript VARCHAR (1000),
    version_num INTEGER NOT NULL DEFAULT 0,
    created_by INTEGER,
    recorded_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_tag, version_num)
);


CREATE TABLE venue (
	id_tag VARCHAR (50) NOT NULL,
	venue_name VARCHAR ( 50 ) NOT NULL,
    venue_county VARCHAR ( 50 ),
	year_built INTEGER,
    version_num INTEGER NOT NULL DEFAULT 0,
    created_by INTEGER,
    recorded_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_tag, version_num)
);

CREATE TABLE referee (
	id_tag VARCHAR (50) NOT NULL,
	full_name VARCHAR (100) NOT NULL,
	dob DATE,
    career_start DATE,
	career_end DATE,
    county VARCHAR ( 50 ),
    version_num INTEGER NOT NULL DEFAULT 0,
    created_by INTEGER,
    recorded_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_tag, version_num)
);


CREATE TABLE team (
	id_tag VARCHAR (50) NOT NULL,
	team_name VARCHAR ( 50 ) NOT NULL,
    sport VARCHAR (12),
	est_year SMALLINT,
    is_county BOOLEAN NOT NULL DEFAULT true,
    main_venue_id VARCHAR (50),
    version_num INTEGER NOT NULL DEFAULT 0,
    created_by INTEGER,
    recorded_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_tag, version_num)
);


CREATE TABLE team_manager (
	id_tag VARCHAR (50) NOT NULL,
	full_name VARCHAR (100) NOT NULL,
	dob DATE,
    position_start DATE,
	position_end DATE,
	team_id VARCHAR (50),
    version_num INTEGER NOT NULL DEFAULT 0,
    created_by INTEGER,
    recorded_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_tag, version_num)
);

CREATE TABLE player (
	id_tag VARCHAR (50) NOT NULL,
	full_name VARCHAR (100) NOT NULL,
	dob DATE,
    career_start DATE,
	career_end DATE,
    typical_position VARCHAR (30),
    team_id VARCHAR (50),
    caps INTEGER,
    version_num INTEGER NOT NULL DEFAULT 0,
    created_by INTEGER,
    recorded_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_tag, version_num)
);

CREATE TABLE match (
	id_tag VARCHAR (50) NOT NULL,
	home_team_id VARCHAR (50),
    away_team_id VARCHAR (50),
    home_team_manager_id VARCHAR (50),
    away_team_manager_id VARCHAR (50),
    home_team_goals INTEGER NOT NULL,
    home_team_points INTEGER NOT NULL,
    away_team_goals INTEGER NOT NULL,
    away_team_points INTEGER NOT NULL,
    match_date DATE,
    match_time TIME,
    championship_id VARCHAR (50),
    championship_round VARCHAR (5),
    is_replay BOOLEAN NOT NULL DEFAULT false,
    venue_id VARCHAR (50),
    half_time BOOLEAN,
    full_time BOOLEAN,
    extra_time BOOLEAN,
    referee_id VARCHAR (50),
    version_num INTEGER NOT NULL DEFAULT 0,
    created_by INTEGER,
    recorded_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_tag, version_num)
);



/* TEST DATA */

INSERT INTO portal_user (google_sub) VALUES ('112547902526737646117');
INSERT INTO championship (id_tag, championship_name, descript) VALUES ('CHAMP_001', 'All-Ireland Hurling Championship', 'The top tier national championship');
INSERT INTO venue (id_tag, venue_name, venue_county, year_built) VALUES ('VEN_001', 'Croke Park', 'Dublin', 1880);
INSERT INTO venue (id_tag, venue_name, venue_county, year_built) VALUES ('VEN_002', 'Dr Cullen Park', 'Carlow', 1936);
INSERT INTO referee (id_tag, full_name, dob, county) VALUES ('REF_001', 'Frank Murphy', '1944-01-05', 'Cork');
INSERT INTO team (id_tag, team_name, sport, est_year, is_county, main_venue_id) VALUES ('TEAM_001', 'Carlow', 'Hurling', 1930, true, 'VEN_002');
INSERT INTO team (id_tag, team_name, sport, est_year, is_county, main_venue_id) VALUES ('TEAM_002', 'Dublin', 'Hurling', 1898, true, 'VEN_001');
INSERT INTO team (id_tag, team_name, sport, est_year, is_county, main_venue_id) VALUES ('TEAM_003', 'BallyBoden St Endas', 'Hurling', 1966, false, 'VEN_001');
INSERT INTO player (id_tag, full_name, dob, team_id, caps) VALUES ('PLAY_001', 'DJ Carey', '1974-01-05', 'TEAM_001', 100);
INSERT INTO team_manager (id_tag, full_name, dob, position_start, team_id) VALUES ('MAN_001', 'Davy Fitzgerald', '1974-07-05', '2014-07-05', 'TEAM_001');
INSERT INTO match 
    (id_tag, home_team_id, away_team_id, home_team_goals, home_team_points, away_team_goals, 
    away_team_points, match_date, championship_id, championship_round, is_replay, 
    venue_id, half_time, full_time, extra_time, referee_id) 
    VALUES ('MATCH_001', 'TEAM_001', 'TEAM_002', 1, 22, 3, 20, '2020-05-05', 'CHAMP_001', 'F', false, 'VEN_001', true, true, true, 'REF_001');

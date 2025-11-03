CREATE TABLE Matches (
    id SERIAL PRIMARY KEY,
    home_team_id INT NOT NULL,
    away_team_id INT NOT NULL,
    referee_id INT,
    stadium_id INT,
    scoreboard INT,
    possession VARCHAR(20),
    expected_goals VARCHAR(20),
    big_chances VARCHAR(20),
    shots VARCHAR(20),
    goalkeeper_saves VARCHAR(20),
    corners VARCHAR(20),
    fouls VARCHAR(20),
    passes VARCHAR(20),
    tackles VARCHAR(20),
    direct_kicks VARCHAR(20),
    yellow_cards INT DEfAULT 0,
    red_cards INT DEFAULT 0,
    match_date TIMESTAMP NOT NULL
);

-- Tabela Team
CREATE TABLE Team (
    id SERIAL PRIMARY KEY,
    team_name VARCHAR(50),
    ranking INT
);

-- Tabela Stadium
CREATE TABLE Stadium (
    id SERIAL PRIMARY KEY,
    stadium_name VARCHAR(100) UNIQUE
);

-- Tabela Referee
CREATE TABLE Referee (
    id SERIAL PRIMARY KEY,
    referee_name VARCHAR(100) UNIQUE
);

-- Tabela Player
CREATE TABLE Player (
    id SERIAL PRIMARY KEY,
    player_name VARCHAR(50),
    team_id INT
);

-- Tabela Injuries
CREATE TABLE Injuries (
    id SERIAL PRIMARY KEY,
    match_id INT,
    player_id INT,
    injury_type VARCHAR(50) DEFAULT 'Não especificado'
);

-- Tabela Rating
CREATE TABLE Rating (
    id SERIAL PRIMARY KEY,
    player_id INT,
    match_id INT,
    rating FLOAT
);


-- Adicionando algumas Foreign Key Constraints
ALTER TABLE Matches ADD FOREIGN KEY(home_team_id) REFERENCES Team(id);
ALTER TABLE Matches ADD FOREIGN KEY(away_team_id) REFERENCES Team(id);
ALTER TABLE Matches ADD FOREIGN KEY(referee_id) REFERENCES Referee(id);
ALTER TABLE Matches ADD FOREIGN KEY(stadium_id) REFERENCES Stadium(id);
ALTER TABLE Rating ADD FOREIGN KEY(player_id) REFERENCES Player(id);
ALTER TABLE Rating ADD FOREIGN KEY(match_id) REFERENCES Matches(id);
ALTER TABLE Player ADD FOREIGN KEY(team_id) REFERENCES Team(id);
ALTER TABLE Injuries ADD FOREIGN KEY(match_id) REFERENCES Matches(id);
ALTER TABLE Injuries ADD FOREIGN KEY(player_id) REFERENCES Player(id);

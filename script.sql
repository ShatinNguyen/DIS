DROP TABLE chess_games;

CREATE TABLE chess_games (
    id VARCHAR(255) PRIMARY KEY NOT NULL,
    rated BOOLEAN,
    created_at VARCHAR(100),
    last_move_at VARCHAR(100),
    turns INT,
    victory_status VARCHAR(255),
    winner VARCHAR(255),
    increment_code VARCHAR(255),
    white_id VARCHAR(255),
    white_rating INT,
    black_id VARCHAR(255),
    black_rating INT,
    moves TEXT,
    opening_eco VARCHAR(255),
    opening_name VARCHAR(255),
    opening_ply INT
);

COPY chess_games(
    id,
    rated, 
    created_at ,
    last_move_at, 
    turns ,
    victory_status, 
    winner ,
    increment_code, 
    white_id ,
    white_rating, 
    black_id ,
    black_rating,
    moves,
    opening_eco,
    opening_name,
    opening_ply) 
FROM 'dataset.csv'
DELIMITER ',' 
CSV HEADER;
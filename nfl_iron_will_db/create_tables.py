#CREATE "nfl_team" TABLE:
cursor.execute('''CREATE TABLE IF NOT EXISTS nfl_team (team_name VARCHAR(30) PRIMARY KEY,
    team_name_short VARCHAR(10),
    team_id CHAR(3),
    team_id_pfr CHAR(3),
    nfl_conf CHAR(3),
    nfl_conf_div VARCHAR(20),
    nfl_conf_pre2002 CHAR(3),
    nfl_conf_div_pre2002 VARCHAR(20));''')
dmconn.commit()

#CREATE "nfl_stadiums" TABLE:
cursor.execute('''CREATE TABLE IF NOT EXISTS nfl_stadium (
    stadium_name VARCHAR(40) PRIMARY KEY,
    stadium_open INT,
    stadium_close INT,
    stadium_cap INT,
    stadium_surface VARCHAR(50),
    stadium_type VARCHAR(15),
    stadium_address VARCHAR(100),
    stadium_location VARCHAR(20),
    stadium_weather_station_code VARCHAR(25),
    stadium_weather_type VARCHAR(10),
    weather_station VARCHAR(15),
    weather_station_name VARCHAR(50),
    weather_station_latitude NUMERIC,
    weather_station_longitude NUMERIC,
    weather_station_elevation NUMERIC
);''')
dmconn.commit()

#CREATE "nfl_games" TABLE:
cursor.execute('''CREATE TABLE IF NOT EXISTS nfl_games (
    game_id VARCHAR(50) PRIMARY KEY NOT NULL,
    game_date DATE NOT NULL,
    game_season CHAR(4) NOT NULL,
    game_week VARCHAR(10) NOT NULL,
    game_neutral_stadium BOOLEAN NOT NULL,
    game_sched_playoff BOOLEAN NOT NULL,
    home_team_score INT NOT NULL,
    away_team_score INT NOT NULL,
    game_team_favorite VARCHAR(50),
    game_favorite_spread FLOAT,
    game_ou_line FLOAT,
    bet_overunder INT,
    game_temp INT,
    game_wind_mph INT,
    game_weather_details VARCHAR(25),
    game_home_team VARCHAR(30),
    game_away_team VARCHAR(30),
    game_stadium  VARCHAR(40),
    game_humidity INT
)''')
dmconn.commit()

#CREATE "placed_bet" TABLE:
cursor.execute('''CREATE TABLE IF NOT EXISTS placed_bet(
    bet_id INT PRIMARY KEY,
    bet_amount NUMERIC NOT NULL,
    bet_on VARCHAR(30) NOT NULL,
    bet_result VARCHAR(4) NOT NULL,
    customer_id INT NOT NULL,
    game_id VARCHAR(50)
    );''')
dmconn.commit()

#CREATE "bet_customer" TABLE:
cursor.execute('''CREATE TABLE IF NOT EXISTS bet_customer(
    customer_id INT PRIMARY KEY,
    customer_fname VARCHAR(50) NOT NULL,
    customer_lname VARCHAR(50) NOT NULL,
    customer_age INT NOT NULL,
    customer_since INT NOT NULL,
    customer_household INT NOT NULL,
    customer_income NUMERIC NOT NULL,
    customer_type VARCHAR(50) NOT NULL,
    customer_mode_color VARCHAR(10) NOT NULL
);''')
dmconn.commit()

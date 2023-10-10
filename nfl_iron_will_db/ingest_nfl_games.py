#INGEST "nfl_games" DATA:
team_id_dict = [['Arizona Cardinals','ARI'],['Phoenix Cardinals','ARI'],['St. Louis Cardinals','ARI'],['Atlanta Falcons','ATL'],['Baltimore Ravens','BAL'],['Buffalo Bills','BUF'],['Carolina Panthers','CAR'],['Chicago Bears','CHI'],['Cincinnati Bengals','CIN'],['Cleveland Browns','CLE'],['Dallas Cowboys','DAL'],['Denver Broncos','DEN'],['Detroit Lions','DET'],['Green Bay Packers','GB'],['Houston Texans','HOU'],['Baltimore Colts','IND'],['Indianapolis Colts','IND'],['Jacksonville Jaguars','JAX'],['Kansas City Chiefs','KC'],['Los Angeles Chargers','LAC'],['San Diego Chargers','LAC'],['Los Angeles Rams','LAR'],['St. Louis Rams','LAR'],['Las Vegas Raiders','LVR'],['Los Angeles Raiders','LVR'],['Oakland Raiders','LVR'],['Miami Dolphins','MIA'],['Minnesota Vikings','MIN'],['Boston Patriots','NE'],['New England Patriots','NE'],['New Orleans Saints','NO'],['New York Giants','NYG'],['New York Jets','NYJ'],['Philadelphia Eagles','PHI'],['Pittsburgh Steelers','PIT'],['Seattle Seahawks','SEA'],['San Francisco 49ers','SF'],['Tampa Bay Buccaneers','TB'],['Houston Oilers','TEN'],['Tennessee Oilers','TEN'],['Tennessee Titans','TEN'],['Washington Commanders','WAS'],['Washington Football Team','WAS'],['Washington Redskins','WAS']]

df2 = pd.read_csv(spread_file)

df2['schedule_season'] = df2['schedule_season'].astype('str')
df2['team_favorite_id'].replace(to_replace=np.nan, value='NULL', inplace=True)
df2['spread_favorite'].replace(to_replace=np.nan, value=420, inplace=True)
df2['over_under_line'] = df2['over_under_line'].replace(r'^\s*$', np.nan, regex=True)
df2['over_under_line'].replace(to_replace=np.nan, value=420, inplace=True)
df2['over_under_line'] = df2['over_under_line'].astype({'over_under_line': float})
df2['weather_temperature'].replace(to_replace=np.nan, value=420, inplace=True)
df2['weather_wind_mph'].replace(to_replace=np.nan, value=420, inplace=True)
df2['weather_humidity'].replace(to_replace=np.nan, value=420, inplace=True)
df2['weather_detail'].replace(to_replace=np.nan, value='NULL', inplace=True)
df2['stadium'] = df2['stadium'].str.replace('\'', '')
df2['bet_overunder'] = np.where(
            df2['score_home'] + df2['score_away'] >= df2['over_under_line'],
            1, 0)
     
for x in df2.index:
    
    team_home_id = None
    team_away_id = None
    team_favorite = 'NULL'
    week_var = None
    game_id = None
    last_week = None

    #Assign team_x their team_id:
    for team in team_id_dict:
        if team[0] == df2['team_home'].loc[x]:
            team_home_id = team[1]

        elif team[0] == df2['team_away'].loc[x]:
            team_away_id = team[1]

        else:
            continue
    
    #Assign Spread Favorite Team ID its associated full name:
    for team2 in team_id_dict:
        if team2[1] == df2['team_favorite_id'].loc[x]:
            team_favorite = team2[0]

    #Prep Weeks for game_id value:        
    if len(df2['schedule_week'].loc[x]) < 2:
        week_var = '0' + df2['schedule_week'].loc[x]

    elif len(df2['schedule_week'].loc[x]) > 2 :
        dflw = pd.read_sql('''select game_id,
                                   game_week
                            from nfl_games
                            where game_week not in ('Wildcard', 'Division', 'Conference', 'Superbowl')
                            order by 1 desc limit 1''', dmconn)

        last_week = dflw['game_week'][0]

        if df2['schedule_week'].loc[x] == 'Wildcard':
            week_var = int(last_week) + 1

        elif df2['schedule_week'].loc[x] == 'Division':
            week_var = int(last_week) + 2

        elif df2['schedule_week'].loc[x] == 'Conference':
            week_var = int(last_week) + 3

        elif df2['schedule_week'].loc[x] == 'Superbowl':
            week_var = int(last_week) + 4

    else:
        week_var = df2['schedule_week'].loc[x]


    game_id = df2['schedule_season'].loc[x] + str(week_var) + '-' + team_home_id + '-' + team_away_id


    cursor.execute('''INSERT INTO nfl_games (game_id,
                                                game_date,
                                                game_season,
                                                game_week,
                                                game_neutral_stadium,
                                                game_sched_playoff,
                                                home_team_score,
                                                away_team_score,
                                                game_team_favorite,
                                                game_favorite_spread,
                                                game_ou_line,
                                                bet_overunder,
                                                game_temp,
                                                game_wind_mph,
                                                game_weather_details,
                                                game_home_team,
                                                game_away_team,
                                                game_stadium,
                                                game_humidity)

                             VALUES ('%s','%s', '%s', '%s','%s', '%s', %d, %d, '%s', %f, %f, %d, %d, %d, '%s', '%s', '%s', '%s', %d)''' % (game_id, df2['schedule_date'].loc[x], df2['schedule_season'].loc[x], df2['schedule_week'].loc[x], df2['stadium_neutral'].loc[x], df2['schedule_playoff'].loc[x] ,df2['score_home'].loc[x], df2['score_away'].loc[x], team_favorite, df2['spread_favorite'].loc[x], df2['over_under_line'].loc[x], df2['bet_overunder'].loc[x] , df2['weather_temperature'].loc[x], df2['weather_wind_mph'].loc[x], df2['weather_detail'].loc[x], df2['team_home'].loc[x], df2['team_away'].loc[x], df2['stadium'].loc[x],df2['weather_humidity'].loc[x]))
    dmconn.commit()
    print("Record ingested for game: %s" % (game_id))
    

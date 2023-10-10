#INGEST "nfl_teams" DATA:
df = pd.read_csv(team_file)

df['team_division'].replace(to_replace=np.nan, value='NULL', inplace=True)
df['team_division_pre2002'].replace(to_replace=np.nan, value='NULL', inplace=True)

for x in df.index:
    cursor.execute('''INSERT INTO nfl_team (team_name,
                                            team_name_short,
                                            team_id,
                                            team_id_pfr,
                                            nfl_conf,
                                            nfl_conf_div,
                                            nfl_conf_pre2002,
                                            nfl_conf_div_pre2002
                                            )
                       VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')''' % (df['team_name'].loc[x],df['team_name_short'].loc[x], df['team_id'].loc[x], df['team_id_pfr'].loc[x], df['team_conference'].loc[x], df['team_division'].loc[x], df['team_conference_pre2002'].loc[x], df['team_division_pre2002'].loc[x]))
    dmconn.commit()
    print("Record ingested for the %s" % (df['team_name'].loc[x]))

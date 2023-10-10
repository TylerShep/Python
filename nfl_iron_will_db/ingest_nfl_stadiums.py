#INGEST "nfl_stadiums" DATA:
df1 = pd.read_csv(stadium_file)

df1['stadium_name'] = df1['stadium_name'].str.replace('\'', '')
df1['stadium_location'].replace(to_replace=np.nan, value='NULL', inplace=True)
df1['stadium_open'].replace(to_replace=np.nan, value=0, inplace=True)
df1['stadium_open'] = df1['stadium_open'].astype('int')
df1['stadium_close'].replace(to_replace=np.nan, value=0, inplace=True)
df1['stadium_close'] = df1['stadium_close'].astype('int')
df1['stadium_type'].replace(to_replace=np.nan, value='NULL', inplace=True)
df1['stadium_address'].replace(to_replace=np.nan, value='NULL', inplace=True)
df1['stadium_address'] = df1['stadium_address'].str.replace('[^a-zA-Z0-9]+', ' ')
df1['stadium_weather_station_code'].replace(to_replace=np.nan, value='NULL', inplace=True)
df1['stadium_weather_type'].replace(to_replace=np.nan, value='NULL', inplace=True)
df1['stadium_capacity'] = df1['stadium_capacity'].str.replace(',','')
df1['stadium_capacity'].replace(to_replace=np.nan, value=0, inplace=True)
df1['stadium_capacity'] = df1['stadium_capacity'].astype('int')
df1['stadium_surface'].replace(to_replace=np.nan, value='NULL', inplace=True)
df1['STATION'].replace(to_replace=np.nan, value='NULL', inplace=True)
df1['NAME'].replace(to_replace=np.nan, value='NULL', inplace=True)
df1['LATITUDE'].replace(to_replace=np.nan, value=0, inplace=True)
df1['LONGITUDE'].replace(to_replace=np.nan, value=0, inplace=True)
df1['ELEVATION'].replace(to_replace=np.nan, value=0, inplace=True)

for x in df1.index:
    cursor.execute('''INSERT INTO nfl_stadium (stadium_name,
                                                stadium_open,
                                                stadium_close,
                                                stadium_cap,
                                                stadium_surface,
                                                stadium_type,
                                                stadium_address,
                                                stadium_location,
                                                stadium_weather_station_code,
                                                stadium_weather_type,
                                                weather_station,
                                                weather_station_name,
                                                weather_station_latitude,
                                                weather_station_longitude,
                                                weather_station_elevation)
                            VALUES ('%s', %d, %d, %d, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %d, %d,  %d)''' % (df1['stadium_name'].loc[x], df1['stadium_open'].loc[x], df1['stadium_close'].loc[x], df1['stadium_capacity'].loc[x], df1['stadium_surface'].loc[x], df1['stadium_type'].loc[x], df1['stadium_address'].loc[x], df1['stadium_location'].loc[x], df1['stadium_weather_station_code'].loc[x], df1['stadium_weather_type'].loc[x], df1['STATION'].loc[x], df1['NAME'].loc[x], df1['LATITUDE'].loc[x], df1['LONGITUDE'].loc[x], df1['ELEVATION'].loc[x]))
    dmconn.commit()
    print("Record ingested for %s stadium" % (df1['stadium_name'].loc[x]))

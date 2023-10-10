#INGEST INTO "iwdm.public.placed_bet":
dmconn.close()

#Connect to ironwill RDB:
conn = pyodbc.connect('DRIVER={' + SECRETS_USU_DRIVER + '};'
                      'Server=' + SECRETS_USU_SERVER + ';'
                      'Database=' + SECRETS_USU_DB + ';'
                      'UID=' + SECRETS_USU_UID + ';'
                      'PWD=' + SECRETS_USU_PWD + ';'
                      'Trusted_Connection=no;')

df = pd.read_sql('''SELECT *
                    FROM betlog;''',conn)
conn.close()

#Reconnect to iwdm DM:
dmconn = psycopg2.connect(
    database= SECRETS_IWDM_DB, 
    user= SECRETS_IWDM_USER, 
    password= SECRETS_IWDM_PASSWORD,
    host= SECRETS_IWDM_HOST, 
    port= SECRETS_IWDM_PORT)

cursor = dmconn.cursor()

for x in df.index:
    cursor.execute('''INSERT INTO placed_bet (bet_id,
                                                bet_amount,
                                                bet_on,
                                                bet_result,
                                                customer_id,
                                                game_id)
                                                
                    VALUES (%d, %d, '%s', NULL, %d, '%s')'''% (df['bet_id'].loc[x], df['bet_amount'].loc[x], df['bet_on'].loc[x], df['customer_id'].loc[x], df['game_id'].loc[x]))
                                                
    dmconn.commit()
    
    bet_id_str = str(df['bet_id'].loc[x])
    print("Betting record id %s ingested" % (bet_id_str))

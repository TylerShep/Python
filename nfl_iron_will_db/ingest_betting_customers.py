#INGEST INTO "iwdm.public.bet_customer":
dmconn.close()

#Connect to ironwill RDB:
conn = pyodbc.connect('DRIVER={' + SECRETS_USU_DRIVER + '};'
                      'Server=' + SECRETS_USU_SERVER + ';'
                      'Database=' + SECRETS_USU_DB + ';'
                      'UID=' + SECRETS_USU_UID + ';'
                      'PWD=' + SECRETS_USU_PWD + ';'
                      'Trusted_Connection=no;')

df = pd.read_sql('''SELECT *
                    FROM customer_table;''',conn)
conn.close()

df['customer_name'] = df['customer_name'].str.replace('\'', '')
df[['customer_fname','customer_lname']] = df['customer_name'].str.split(pat= ' ',n=1, expand=True)

#Reconnect to iwdm DM:
dmconn = psycopg2.connect(
    database= SECRETS_IWDM_DB, 
    user= SECRETS_IWDM_USER, 
    password= SECRETS_IWDM_PASSWORD,
    host= SECRETS_IWDM_HOST, 
    port= SECRETS_IWDM_PORT
)
cursor = dmconn.cursor()

for x in df.index:
    cursor.execute('''INSERT INTO bet_customer (customer_id,
                                                customer_fname,
                                                customer_lname,
                                                customer_age,
                                                customer_since,
                                                customer_household,
                                                customer_income,
                                                customer_type,
                                                customer_mode_color)

                      VALUES (%d, '%s', '%s', %d, %d, %d, %d, '%s', '%s')''' % (df['customer_id'].loc[x], df['customer_fname'].loc[x], df['customer_lname'].loc[x], df['customer_age'].loc[x], df['customer_since'].loc[x], df['household_size'].loc[x], df['customer_income'].loc[x], df['customer_type'].loc[x], df['mode_color'].loc[x]))
    dmconn.commit()
    
    cus_id_str = str(df['customer_id'].loc[x])
    print("Betting customer_id %s record ingested" % (cus_id_str))

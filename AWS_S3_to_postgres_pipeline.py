import boto3
import pandas as pd
import psycopg2

key_id='secrets.s3.cfbdata.id'
secret_key='secrets.s3.cfbdata.sk'
region='secrets.s3.cfbdata.region'


#CREATE AWS S3 CONNECTION (Use 'Resource')
s3 = boto3.resource(
    's3',
    aws_access_key_id= SECRETS_KEY_ID,
    aws_secret_access_key= SECRETS_KEY,
    region_name=region)

client = boto3.client('s3')


#LIST ALL OBJECTS/BUCKETS
for bucket in s3.buckets.all():
    my_bucket = s3.Bucket(bucket.name)
    
    bucket_name = bucket.name
    print(bucket_name)
    
    
#CONNECT TO POSTGRES DB 'cfbdata'
conn = psycopg2.connect(
    database="secrets.cfbdata,db", 
    user='secrets.cfbdata.user', 
    password='secrets.cfbdata.password', 
    host='secrets.cfbdata.host', 
    port= '5432')
  
cursor = conn.cursor()


#READ ALL CSVs FROM EXISTING BUCKET; LOAD INTO PANDAS all CSVs from existing bucket; load into pandas DF
s3 = boto3.client('s3', aws_access_key_id=key_id,
                  aws_secret_access_key=secret_key,
                  region_name=region)

# get list of all CSV files in bucket
objects = s3.list_objects(Bucket= bucket_name, Prefix='', Delimiter='/')
csv_files = [obj['Key'] 
for obj in objects.get('Contents') if obj['Key'].endswith('.csv')]

# read each CSV file into a pandas dataframe
for file in csv_files:
    if file == 'cfb22.csv':
        obj = s3.get_object(Bucket='cfbdata', Key=file)
        
        #perform pandas cleanup
        df = pd.read_csv(obj['Body'])
        df[['Win', 'Loss']] = df["Win-Loss"].apply(lambda x: pd.Series(str(x).split("-")))
        df['Conference'] = df['Team'].apply(lambda st: st[st.find("(")+1:st.find(")")])
        df['Name'] = df['Team'].str.split('(').str[0]
        df['Team Name'] = df['Name'].str.rstrip()
        cfbdf = df[['Team Name','Conference','Games', 'Win','Loss','Off Rank','Def Rank']]
        
        print(file)
        print(cfbdf)
        
        
        for x in cfbdf.index:
                cursor.execute("""INSERT INTO cfb_team_stats (team_name, team_conference, tot_games, tot_win, tot_loss, off_rank, def_rank, from_file) 
                                      VALUES ('%s','%s',d%, d%, d%, d%, d%, d%, '%s')""" % ( cfbdf['Team Name'].loc[x], cfbdf['Conference'].loc[x], cfbdf['Games'].loc[x], cfbdf['Win'].loc[x], cfbdf['Loss'].loc[x], cfbdf['Off Rank'].loc[x], cfbdf['Def Rank'].loc[x], file))
                conn.commit()

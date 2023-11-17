# =============================================
# AUTHOR:      Tyler Shepherd
# CREATE DATE: 2023-11-17
# LAST UPDATE DATE:
# PROBLEM: Due to tasks being backed up, sometimes a stream snapshot wont go off and populate a stats table with yesterdays data. this code block will be used to account for missed days and will start a backfill
# DESCRIPTION: 
# Create a DB connection to where a stats_table (postgres) is storing snapshot data by day
# Using DB connection, query for the lastest date in the table, save to a pandas dictionary, and return as a single datetime value
# Check to see if the returned datetime value is yesteray; pass if and continue normally in stream pipeline if it is. if it isn't, create a list of all dates between the returned date and yesterday. return this date list.
# Loop through list of dates in stream pipeline to backfill dates missed
# =============================================


from datetime import datetime, timedelta
from psycopg2 import OperationalError
import psycopg2
import pandas as pd


def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
    except OperationalError as e:
        print(f"The error '{e}' occurred")

    return connection


def get_last_stats_date(connection):
    df = pd.read_sql('''select es.stats_date
                        from stat_table_1 es
                        group by es.stats_date
                        order by 1 desc limit 1;''', connection)
    
    latest_date = df['es.stats_date'].loc[0]

    return latest_date



def process_date(input_date):
    # Convert string to datetime object
    try:
        input_date = datetime.strptime(input_date, '%Y-%m-%d')
    except ValueError:
        return "Invalid Date"

    # Calculate difference in days
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    date_diff = (yesterday - input_date).days

    # Check the difference
    if date_diff == 0:
        # Proceed with the rest of the code
        pass
    else:
        # Create a list of dates from the input date to yesterday
        date_list = [(input_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(date_diff + 1)]
        return date_list

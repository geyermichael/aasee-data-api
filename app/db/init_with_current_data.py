"""
This file is only to use for creating a database with the current data.
"""

from mysql.connector import Error
import pandas as pd
from datetime import datetime
import requests
import connection
import create_db

def create_table_sensor_data():
    try:
        con = connection.establish_con()
        if con.is_connected():
            cursor = con.cursor()
            sql_statement = """
                CREATE TABLE sensor_data (
                    id int auto_increment AUTO_INCREMENT NOT NULL,
                    datum datetime,
                    wassertemperatur float,
                    ph_wert float,
                    sauerstoffgehalt float,
                    aussentemperatur float,
                    PRIMARY KEY (id)
                );
                CREATE INDEX index_datum ON sensor_data (datum);
                """
            result = cursor.execute(sql_statement, multi=True)
            for res in result:
                    print("Running query: ", res)  # Will print out a short representation of the query
                    print(f"Affected {res.rowcount} rows" ) 
            con.commit()
            print(
                f'👍 Table sensor_date created\n')
    except Error as error:
        print("🚫 Error while connecting to MySQL", error)
    finally:
        connection.close_con(con, cursor) 
        
def insert_sensor_data():  
    # only for testing
    #
    dev_num_of_entries = 25 # set number of table entries.
    dev_exit = False # helper to exit outer for-loop
    # --------------------------------------------------
      
    # list of data to insert into database
    data = []
    
    # get current list of csv files from muenster datahub aasee-monitoring
    # see: https://github.com/od-ms/aasee-monitoring/tree/main
    files = pd.read_json('https://api.github.com/repos/od-ms/aasee-monitoring/contents/data') 
    
    # loop through all files
    for index, row in files.iterrows():
        
        # get csv content of single file
        df = pd.read_csv(row["download_url"])
        
        # !!!
        # run follwing if case for testing
        # if(dev_exit == True):
        #     break
         # !!!
        
        # loop through elements in csv file
        for elem in df.itertuples():
            
            # create datetime from column "Datum"
            date_sensor = datetime.strptime(elem[1], '%Y-%m-%d %H:%M')
            
            # get weather data for certain date
            response = requests.get(f'https://api.brightsky.dev/weather?lat=51.95&lon=7.6&date={str(date_sensor.date())}')
            json = response.json()
            
            # !!!
            # run following if case for testing
            # if(elem[0] == dev_num_of_entries):
            #     dev_exit = True
            #     break
            # !!!
            
            temperature = None
            for entry in json["weather"]:
                date_temp =  datetime.strptime(entry["timestamp"], '%Y-%m-%dT%H:%M:%S%z') 
                if(date_sensor.hour == date_temp.hour):
                    temperature = entry["temperature"]
            
            tup = (f'{str(date_sensor)}', elem[2], elem[3], elem[4], temperature)
            data.append(tup)
            print(tup) # print to see the progress
    
    try:
        con = connection.establish_con()
        if con.is_connected():
            
            cursor = con.cursor()
            sql_statement = f"""
                INSERT INTO sensor_data (
                    datum,
                    wassertemperatur,
                    ph_wert,
                    sauerstoffgehalt,
                    aussentemperatur
                ) VALUES (%s, %s, %s, %s, %s)
            """
            cursor.executemany(sql_statement, data)
            con.commit()
            print(
                f'👍 Insert data into sensor_data\n')
    except Error as error:
        print("🚫 Error while connecting to MySQL", error)
    finally:
        connection.close_con(con, cursor)         
 
# RUN
create_db.create_database()
create_table_sensor_data()
insert_sensor_data()
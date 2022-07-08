import os
from dotenv import load_dotenv
from mysql.connector import Error
import connection

load_dotenv()
db_name = os.getenv('DB_NAME')

def create_database():
    try:
        con = connection.establish_con(with_db_name=False)
        if con.is_connected():
            cursor = con.cursor()
            cursor.execute(f'CREATE DATABASE IF NOT EXISTS `{db_name}`;')
            con.commit()
            print(f'Database created with name: {db_name}')
            cursor.close()
            con.close()
    except Error:
        print("🚫 Error while connecting to MySQL")
     
create_database()      
import os
from dotenv import load_dotenv
import mysql
from mysql.connector import Error

load_dotenv() # load env vars

# set env vars
env = os.getenv('ENV')
if env == 'dev':
    db_host = os.getenv('DB_DEV_HOST')
else:   
    db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_pw = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
con_timeout = 30 # set a connection timeout in seconds

def establish_con(with_db_name: bool = True) -> mysql.connector.connection.MySQLConnection:
    """
    Try to establish a database connection.

    Args:
        with_db_name = True (bool): indicates if a already existing database should be used.

    Returns:
        mysql.connector.connection.MySQLConnection
    """
    try:
        if with_db_name == True:
            return mysql.connector.connect( host=db_host, user=db_user, password=db_pw, database=db_name, connection_timeout=con_timeout )
        if with_db_name == False:     
            return mysql.connector.connect( host=db_host, user=db_user, password=db_pw, connection_timeout=con_timeout )
    except Error as error:
        print('🚫 Error while connecting to MySQL.\nERROR', error, f'\nNo connection established after {con_timeout}ms.\n')  
        
        if f"Unknown database '{db_name}'" in str(error): # in case the database does not exist
            if env == 'dev':
                print('💡 Seems you not finished the initialization. Please use the command `make app-dev-init`.')  
            
        
        raise Exception('No MySQL connection.') # rais exception if no connection established

def close_con(con, cursor):
    """
    Close the database connection.

    Args:
        con (mysql.connection): the databse connection
        cursor (mysql.connection.cursor): the database connection cursor

    """
    if con.is_connected(): 
        cursor.close()
        con.close()
        print("🤝 MySQL connection was closed")

from fastapi import APIRouter
from mysql.connector import Error
from datetime import datetime
from app.db import connection
from app.api.utils import on_error, error_response

router = APIRouter()

@router.get('/raw-data', tags=['💿 Raw Data'])
def get_raw_data():
    """
    This endpoint returns all the raw data stored in the database. 
    """
    
    try:
        con = connection.establish_con()
       
        cursor = con.cursor(dictionary=True)
        cursor.execute("select * from sensor_data")  
        data = cursor.fetchall()
        
        return data
    except Error as error:
        connection.close_con(con, cursor)
        on_error(error, __name__)
    except Exception as error:
        on_error(error, __name__)

@router.get('/raw-data/id/{data_id}', tags=['💿 Raw Data'])
def get_raw_data_by_id(data_id: int):
    """
    This endpoint returns a single dataset based on a given id. 
    """
    
    try:
        con = connection.establish_con()
        cursor = con.cursor(dictionary=True)
        cursor.execute(f"select * from sensor_data where id = {data_id}")
        data = cursor.fetchall()
        return data
    except Error as error:
        connection.close_con(con, cursor)
        on_error(error, __name__)
    except Exception as error:
        on_error(error, __name__)

@router.get('/raw-data/date/{date}', tags=['💿 Raw Data'])
def get_raw_data_by_date(date: str):
    """
    This endpoint returns the raw data of a single day based on a given date.
    
    Date format has to be like: YYYY-mm-dd // e.g. 2022-02-24
    """
    
    try:
        date = datetime.strptime(date, '%Y-%m-%d') # try to create a datetime object
    except:
        date_error_res = {
        'hint': "Try date format: YYYY-mm-dd"
        }
        date_error_res.update(error_response)
        return date_error_res # return case if wrong date format
    
    try:
        con = connection.establish_con()
        cursor = con.cursor(dictionary=True)
        cursor.execute(f"select * from sensor_data where datum between '{date.date()}T00:00:00' and '{date.date()}T23:59:59'")
        data = cursor.fetchall()
        return data
    except Error as error:
        connection.close_con(con, cursor)
        on_error(error, __name__)
    except Exception as error:
        on_error(error, __name__)

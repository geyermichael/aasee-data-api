from fastapi import APIRouter, HTTPException
from datetime import datetime
import json
from app.analytics import analytics
from app.api.utils import on_error, error_response

router = APIRouter()

@router.get('/average', tags=['📊 Analytics Results'])
def get_average():
    """
    This endpoint returns the calculated average values.
    
    """
    try:
        result = analytics.calculate_average()
        return {
            'success': 'true',
            'message': 'Calculated average values.',
            'data': result
            }
    except Exception as error:
        on_error(error, __name__)

@router.get('/average/date-range', tags=['📊 Analytics Results'])
def get_average_by_date_range(start_date: str, end_date: str):
    """
    This endpoint returns the calculated average values between two given dates.
    
    Date format has to be like: YYYY-mm-dd // e.g. 2022-02-24
    """
    try:
        check_start_date = datetime.strptime(start_date, '%Y-%m-%d') # try to create a datetime object
        check_end_date = datetime.strptime(end_date, '%Y-%m-%d') # try to create a datetime object
        if start_date == end_date or check_start_date > check_end_date:
            raise
    except:
        date_error_res = {
        'hint': "Check: Try date format: YYYY-mm-dd. Same dates are not allowed. End date cannot be before start date."
        }
        date_error_res.update(error_response)
        return date_error_res # return case if wrong date format
    
    try:
        result = analytics.calculate_range_average(start_date, end_date)
        return {
            'success': 'true',
            'message': 'Calculated average values by date range.',
            'data': result
            }
    except Exception as error:
        on_error(error, __name__)

@router.get('/date-range', tags=['📊 Analytics Results'])
def get_date_range(start_date: str, end_date: str):
    """
    This endpoint returns the data between two given dates.
    
    Date format has to be like: YYYY-mm-ddTHH:MM // e.g. 2022-02-24T09:12
    """
    
    try:
        check_start_date = datetime.strptime(start_date, '%Y-%m-%dT%H:%M') # try to create a datetime object
        check_end_date = datetime.strptime(end_date, '%Y-%m-%dT%H:%M') # try to create a datetime object
        if start_date == end_date or check_start_date > check_end_date:
            raise
    except:
        date_error_res = {
        'hint': "Check: Try date format: YYYY-mm-ddTHH:MM. Same dates are not allowed. End date cannot be before start date."
        }
        date_error_res.update(error_response)
        return date_error_res # return case if wrong date format
    
    try:
        result = analytics.select_time_range(start_date, end_date)
        res = result.to_json(orient="records")
        parsed_res = json.loads(res)
        return {
            'success': 'true',
            'message': f'Sensor data between {start_date} and {end_date}.',
            'data': parsed_res
            }
    except Exception as error:
        on_error(error, __name__)

@router.get('/data-gaps', status_code=200, tags=['📊 Analytics Results'])
def get_data_gaps():
    """
    This endpoint returns days where no data is present.
    """
    
    try:
        result = analytics.find_data_gaps()
        return {
            'success': 'true',
            'message': 'Missing sensor data on these days.',
            'data': result}
    except Exception as error:
        on_error(error, __name__)
          
@router.get('/predict', tags=['📊 Analytics Results'])
def get_predicted_watertemp(month: int, day: int, temp: int, interpolation : bool = False):
    """
    This endpoint returns a predicted water temperature on a single day by a given outdoor temperature.\n
    *Missing data is not fixed by default.*
    <br><br>
    
    To predict every day we use interpolation.
    Set the query parameter intepolation to true for using it.
    
    **Try it with one of the missing dates by 'Get Data Gaps'.**
    """
    
    success_res_message = f'The predicted water temperature on day: {day} of month: {month}, by the given outdoor temperature of {temp}˚ Celsius at this day.'
    
    try:
        if interpolation == False:
            print(interpolation)
            result = analytics.predict_wassertemperatur(month, day, temp)
            print(result)
            if result == 'nan': # check in case results is of string 'nan' due to missing data
                return {
                    'hint': f'Please try /api/v1/predict?interpolation=true&month={month}&day={day}&temp={temp}',
                    'success': 'false',
                    'message': f'Cannot predicted water temperature on day: {day} of month: {month}, by the given outdoor temperature of {temp}˚ Celsius at this day due to missing sensor data.',
                    'data': result
                }
            else:
                return {
                    'success': 'true',
                    'message': success_res_message,
                    'data': result
                }
                
        else:
            print('do')
            result = analytics.predict_wassertemperatur_daily(month, day, temp)
            print(result)
            return {
                'success': 'true',
                'message': success_res_message,
                'data': result
            }      
    except Exception as error:
        on_error(error, __name__)
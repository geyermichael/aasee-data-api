from fastapi import HTTPException

error_response = {
    'success': 'false',
    'message': '🚫 Something went wrong!'
}

def on_error(error, func_name):
    print(f"🚫 Error executing {func_name}", error)
    if "Table 'aasee_database.sensor_data' doesn't exist" in str(error):
        print('💡 Seems there is no data in the database. Something might went wrong.')
    raise HTTPException(status_code=500, detail=error_response)
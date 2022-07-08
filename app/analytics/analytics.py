import os
from dotenv import load_dotenv
import pandas as pd
import datetime
load_dotenv()
env = os.getenv('ENV')

curr_work_directory = os.getcwd()
filepath_response = curr_work_directory + r"\app\analytics\response.json"

def get_dataframe() -> pd.core.frame.DataFrame:
    """ Get raw data from endpoint (or json File) and write it into dataframe.

    Returns:
        pd.core.frame.DataFrame: Data set.
    """
    # if env == 'dev':
    #     return pd.read_json('http://0.0.0.0:8042/api/v1/raw-data')
    # else:
    #     return pd.read_json('http://0.0.0.0:8000/api/v1/raw-data')
    
    try:
        df = pd.read_json('http://0.0.0.0:8000/api/v1/raw-data')
    except:
        df = pd.read_json(filepath_response)
    return df

def select_time_range(start_date: str, end_date: str) -> pd.core.series.Series:
    """ Search into raw data between start and end date. 

    Args:
        start_date (str): start date for search.
        end_date (str): end date for search.

    Returns:
        pd.core.frame.DataFrame: 
    """
    df = get_dataframe()
    mask = (start_date < df["datum"]) & (df["datum"] <= end_date)
    return df.loc[mask]

def calculate_average() -> pd.core.series.Series:
    """Calculate average of total data set.

    Returns:
        pd.core.series.Series: average of every column in data set (without datetime and id columns).
    """
    df = get_dataframe()
    return df[df.columns[2:]].mean()

def calculate_range_average(start_date: str, end_date: str) -> pd.core.frame.DataFrame:
    """Calculate average of given data section.

    Args:
        start_date (str): start date for data section.
        end_date (str): end date for data section.

    Returns:
        pd.core.frame.DataFrame: average of every column in data section (without datetime and id columns).
    """
    df = select_time_range(start_date, end_date)
    return df[df.columns[2:]].mean()

def calculate_difference(df_column1: pd.core.series.Series, df_column2: pd.core.series.Series) -> pd.core.frame.DataFrame:
    """Calculate difference of two given data sets.

    Args:
        df_column1 (pd.core.series.Series): first data set.
        df_column2 (pd.core.series.Series): second data set.

    Returns:
        pd.core.frame.DataFrame: Difference of two given data sets.
    """
    return df_column1 - df_column2

def data_preprocessing(df: pd.core.frame.DataFrame,column_name: str, min_range: int, max_range: int) -> pd.core.frame.DataFrame:
    """ Find outliers and replace outliers with previous value.

    Args:
        df (pd.core.frame.DataFrame): data set for preprocessing.
        column_name (str): Select column for preprocessing.
        min_range (int): Set minimum value for outlier detection.
        max_range (int): Set maximum value for outlier detection.

    Returns:
        pd.core.frame.DataFrame: corrected data column (outliers eliminated).
    """
    df[column_name] = [df[column_name][_] if min_range < df[column_name][_] < max_range else df[column_name][_-1] for _ in df.index]
    return df[column_name]

def create_lookup_table() -> str:
    """Create lookup table (difference calculation) of given data set and save results in json file.

    Returns:
        str: Results (difference) in json format.
    """
    df = get_dataframe()
    df['wassertemperatur'] = data_preprocessing(df, 'wassertemperatur', 0, 50)
    df['differenz'] = calculate_difference(df['wassertemperatur'],df['aussentemperatur'])
    filepath_lookup_table = "./app/analytics/lookup_table_aasee_weather.json"
    df.to_json(filepath_lookup_table)
    return df.to_json()

def create_lookup_table_daily() -> str:
    """Create lookup table (difference calculation) of interpolated data set and save results in json file.

    Returns:
        str: Results (difference) in json format.
    """
    df = interpolate_data()
    df['wassertemperatur'] = data_preprocessing(df, 'wassertemperatur', 0, 50)
    df['differenz'] = calculate_difference(df['wassertemperatur'],df['aussentemperatur'])
    filepath_lookup_table_daily = "./app/analytics/lookup_table_daily_aasee_weather.json"
    df.to_json(filepath_lookup_table_daily)
    return df.to_json()

def predict_wassertemperatur(predicted_month: int, predicted_day: int, temperature: float) -> str:
    """ Predict water temperature for a given date (with lookup table).

    Args:
        predicted_month (int): Set month for prediction horizon.
        predicted_day (int): Set day for prediction horizon.
        temperature (float): Set outside temperature for predicted horizon.

    Returns:
        str: Predicted water temperature for given date.
    """
    df_lookup_table = pd.read_json('./app/analytics/lookup_table_aasee_weather.json')
    df_lookup_table['datum'] = pd.to_datetime(df_lookup_table['datum'])
    mask = (df_lookup_table['datum'].dt.month == predicted_month) & (df_lookup_table['datum'].dt.day == predicted_day)
    difference = df_lookup_table[mask]['differenz'].mean()
    return str(temperature + difference)

def predict_wassertemperatur_daily(predicted_month: int, predicted_day: int, temperature: float) -> str:
    """Predict water temperature for a given date (with interpolated lookup table).

    Args:
        predicted_month (int): Set month for prediction horizon.
        predicted_day (int): Set day for prediction horizon.
        temperature (float): Set outside temperature for predicted horizon.

    Returns:
        str: Predicted water temperature for given date.
    """
    df_lookup_table = pd.read_json('./app/analytics/lookup_table_daily_aasee_weather.json')
    mask = []
    list_years = list(df_lookup_table.index.year)
    for data_year in list(dict.fromkeys(list_years)):
        if mask == []:
            mask = (df_lookup_table.index == datetime.datetime(data_year,predicted_month, predicted_day))
        else:
            mask = (mask) | (df_lookup_table.index == datetime.datetime(data_year,predicted_month, predicted_day))
    difference = df_lookup_table[mask]['differenz'].mean()
    return str(temperature + difference)

def find_data_gaps() -> list:
    """Search in total data set for missing values. Each day should have a data set.

    Returns:
        list: Non-existing days in data set.
    """
    df = get_dataframe()
    df['datum'] = pd.to_datetime(df['datum'])
    start_date = df['datum'][0]
    end_date = df['datum'][df.index[-1]]
    time_vector = pd.date_range(start_date,end_date, freq="D")
    time_vector = time_vector.to_pydatetime()
    data_gaps, data_elements = [],[]
    for _ in time_vector:
        mask = (df['datum'].dt.year ==_.year) & (df['datum'].dt.month == _.month) & (df['datum'].dt.day ==_.day)
        if (len(df[mask]) == 0):
            data_gaps.append(_.date())
    return data_gaps

def interpolate_data() -> pd.core.frame.DataFrame:
    """Linear interpolation over non-existing days in data set. 

    Returns:
        pd.core.frame.DataFrame: Interpolated data set with given data for every date.
    """
    df = get_dataframe()
    df['datum'] = pd.to_datetime(df['datum'])
    df_daily = df.groupby(pd.Grouper(key='datum',freq='1D')).mean()
    df_daily_interpolated = df_daily.interpolate()
    return df_daily_interpolated[df_daily_interpolated.columns[1:]]

# only for debugging
"""
create_lookup_table_daily()
calculate_average()
df_return = select_time_range("2021-05-18T22:00","2021-05-18T23:00")
print(df_return)

wassertemp = predict_wassertemperatur_daily(9, 25, 2)
print(wassertemp)
wassertemp = predict_wassertemperatur(9, 25, 2)
print(wassertemp)

create_lookup_table()

data_gaps = find_data_gaps()
print(data_gaps)
interp = interpolate_data()
print(interp)
df_return = select_time_range('2021-05-18T22:00','2021-05-18T23:00')
wassertemp = predict_wassertemperatur(9, 23, 2)
print(wassertemp)
avg = calculate_average()
print(avg)
"""
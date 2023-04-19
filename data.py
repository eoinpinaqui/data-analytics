# Library imports
import pandas as pd


# Get the wind speeds for given years
def get_wind_speeds_for_years(file: str, years: list) -> dict:
    df = pd.read_csv(file)

    result = {str(year): [] for year in years}
    for index, row in df.iterrows():
        for year in years:
            if str(year) in row['date']:
                result[str(year)].append(int(row['wdsp']))

    return result


# Get the wind speeds for a given year
def get_wind_speeds_for_year(file: str, year: int) -> list:
    df = pd.read_csv(file)

    result = []
    for index, row in df.iterrows():
        if str(year) in row['date']:
            result.append(int(row['wdsp']))

    return result


# Get the wind speeds for a given month in a given year
def get_wind_speeds_for_year_and_month(file: str, year: int, month: str) -> list:
    df = pd.read_csv(file)

    result = []
    for index, row in df.iterrows():
        if str(year) in row['date'] and month in row['date']:
            result.append(int(row['wdsp']))

    return result

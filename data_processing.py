# Library imports
import pandas as pd


# Get the wind speeds for given years
def get_wind_speeds_for_years(file: str, years: list) -> dict:
    df = pd.read_csv(file)

    result = {str(year): [] for year in years}
    for index, row in df.iterrows():
        for year in years:
            if str(year) in row['date']:
                try:
                    result[str(year)].append(int(row['wdsp']))
                except ValueError:
                    continue

    return result


# Get the wind speeds for the months of a given year
def get_monthly_wind_speeds_for_year(file: str, years: list) -> dict:
    df = pd.read_csv(file)

    result = {str(year): {
        'Jan': [],
        'Feb': [],
        'Mar': [],
        'Apr': [],
        'May': [],
        'Jun': [],
        'Jul': [],
        'Aug': [],
        'Sep': [],
        'Oct': [],
        'Nov': [],
        'Dec': []}
        for year in years}

    for index, row in df.iterrows():
        for year in years:
            if str(year) in row['date']:
                month = row['date'][3:6].capitalize()
                try:
                    result[str(year)][month].append(float(row['wdsp']))
                except ValueError:
                    continue

    return result

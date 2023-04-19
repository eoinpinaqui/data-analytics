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


# Get the seasonal wind speeds for a given year
spring = ['jan', 'feb', 'mar']
summer = ['apr', 'may', 'jun']
autumn = ['jul', 'aug', 'sep']
winter = ['oct', 'nov', 'dec']
seasons = {'Spring': spring, 'Summer': summer, 'Autumn': autumn, 'Winter': winter}


def get_seasonal_wind_speeds_for_year(file: str, years: list) -> dict:
    df = pd.read_csv(file)

    result = {str(year): {'Spring': [], 'Summer': [], 'Autumn': [], 'Winter': []} for year in years}
    for index, row in df.iterrows():
        for year in years:
            if str(year) in row['date']:
                for season, months in seasons.items():
                    for month in months:
                        if month in row['date']:
                            try:
                                result[str(year)][season].append(int(row['wdsp']))
                            except ValueError:
                                continue

    return result


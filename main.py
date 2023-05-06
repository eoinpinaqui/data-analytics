# Local imports
from model import WeibullDistribution, plot_weibull_pdf, plot_weibull_mean_against_threshold
from data_processing import get_seasonal_wind_speeds_for_year

# Mappings of station names to their csv files
stations = {
    'Claremorris': './data/claremorris.csv',
    'Dunsany': './data/dunsany.csv',
    'Finner': './data/finner.csv',
    'Gurteen': './data/gurteen.csv',
    'Valentia': './data/valentia.csv'
}


# Read all the data for the given years
def read_data(years: list):
    wbs = {}
    for station, file in stations.items():
        wbs[station] = {}
        data = get_seasonal_wind_speeds_for_year(file, years)
        for year in data:
            year = str(year)
            wbs[station][year] = {}
            year_data = []
            for season in data[year]:
                year_data += data[year][season]
                wbs[station][year][season] = WeibullDistribution(f'{season}', data[year][season])
            wbs[station][year]['full_year'] = WeibullDistribution(f'Full year', year_data)
    return wbs


# The main function
def main():
    # Read in all of the data and plot the pdfs
    wbs = read_data([2018, 2019, 2020, 2021, 2022])

    # Plot the average wind speed for each station in the given years
    for station in wbs:
        for year in wbs[station]:
            wbs_to_plot = []
            for season in wbs[station][year]:
                wbs_to_plot.append(wbs[station][year][season])
            plot_weibull_mean_against_threshold(wbs_to_plot, station, year)


if __name__ == '__main__':
    main()

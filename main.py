# Local imports
from model import WeibullDistribution, plot_weibull_pdf, plot_weibull_cdfs
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
    wbs = []
    for station, file in stations.items():
        data = get_seasonal_wind_speeds_for_year(file, years)
        for year in data:
            year_data = []
            for season in data[year]:
                year_data += data[year][season]
                wbs.append(WeibullDistribution(f'{station} {season} {year}', data[year][season]))
            wbs.append(WeibullDistribution(f'{station} {year}', year_data))
    return wbs


# The main function
def main():
    # Read in all of the data and plot the pdfs
    wbs = read_data([2018, 2020, 2022])
    for wb in wbs:
        plot_weibull_pdf(wb)

    # Plot CDFs for the seasons of each year

    '''
    to_plot = []
    for wb in wbs:
        if '2018' in wb.name:
            to_plot.append(wb)

    plot_weibull_cdfs(to_plot)
    '''


if __name__ == '__main__':
    main()

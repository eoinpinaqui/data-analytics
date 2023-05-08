# Local imports
from model import WeibullDistribution, plot_weibull_pdf, plot_weibull_mean_against_threshold
from data_processing import get_monthly_wind_speeds_for_year

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
        total_5_year = []
        wbs[station] = {}
        data = get_monthly_wind_speeds_for_year(file, years)
        for year in data:
            year = str(year)
            wbs[station][year] = {}
            year_data = []
            for month in data[year]:
                year_data += data[year][month]
                wbs[station][year][month] = WeibullDistribution(f'{month}', data[year][month])
            wbs[station][year]['full_year'] = WeibullDistribution(f'Full year', year_data)
            total_5_year += year_data
            wbs[station]['five_year'] = WeibullDistribution(f'Five year', total_5_year)
    return wbs


# The main function
def main():
    # Read in all of the data and plot the pdfs
    wbs = read_data([2018, 2019, 2020, 2021, 2022])

    # Plot the average wind speed for each station in the given years
    for station in wbs:
        for year in wbs[station]:
            if year == 'five:year':
                continue
            print(f'\n\n\n\n{station}:')
            print(f'Total 5 years = '
                  f'Mean: {wbs[station]["five_year"].mean}, '
                  f'Std: {wbs[station]["five_year"].std}, '
                  f'Entries: {len(wbs[station]["five_year"].data)}')
            print(f'\n\n{station} {year}')
            wbs_to_plot = []
            for month in wbs[station][year]:
                print(f'{wbs[station][year][month].name} = '
                      f'Mean: {wbs[station][year][month].mean}, '
                      f'Std: {wbs[station][year][month].std}, '
                      f'Entries: {len(wbs[station][year][month].data)}')
                wbs_to_plot.append(wbs[station][year][month])
            plot_weibull_mean_against_threshold(wbs_to_plot, station, year)


if __name__ == '__main__':
    main()

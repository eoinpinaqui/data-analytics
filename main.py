# Local imports
from model import WeibullDistribution, plot_weibull_pdf, plot_weibull_mean_against_threshold, plot_mean_and_max_energy_wind_speeds
from data_processing import get_monthly_wind_speeds_for_year

# Library imports
import statistics

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
            wbs[station][year]['full_year'] = WeibullDistribution(f'{year}', year_data)
            total_5_year += year_data
        wbs[station]['five_year'] = WeibullDistribution(f'{station}', total_5_year)
    return wbs


# The main function
def main():
    # Read in all of the data and plot the pdfs
    wbs = read_data([2018, 2019, 2020, 2021, 2022])

    # Plot all PDFs
    for station in wbs:
        plot_weibull_pdf(wbs[station]['five_year'], station, '', '')

        for year in wbs[station]:
            if year == 'five_year':
                continue

            plot_weibull_pdf(wbs[station][year]['full_year'], station, year, '')

            for month in wbs[station][year]:
                if month == 'full_year':
                    continue

                plot_weibull_pdf(wbs[station][year][month], station, year, month)

    # Plot means and stds
    wbs_to_plot = []
    for station in wbs:
        wbs_to_plot.append(wbs[station]['five_year'])
    plot_weibull_mean_against_threshold(wbs_to_plot, 'All stations', '2018-22')

    for station in wbs:
        wbs_to_plot = []
        for year in wbs[station]:
            if year == 'five_year':
                continue
            wbs_to_plot.append(wbs[station][year]['full_year'])
        plot_weibull_mean_against_threshold(wbs_to_plot, station, '2018-22')
        plot_mean_and_max_energy_wind_speeds(wbs_to_plot, station, '2018-22')

    for station in wbs:
        for year in wbs[station]:
            if year == 'five_year':
                continue
            wbs_to_plot = []
            for month in wbs[station][year]:
                if month == 'full_year':
                    continue
                wbs_to_plot.append(wbs[station][year][month])
            plot_weibull_mean_against_threshold(wbs_to_plot, station, year)
            plot_mean_and_max_energy_wind_speeds(wbs_to_plot, station, year)

    # The following legacy code is commented out, but generated the logs for all results tables
    '''
    # Plot the PDF for Claremorris over the five years
    plot_weibull_pdf(wbs['Claremorris']['five_year'])

    # Plot the PDF for each year at each station
    print(' ')
    for station in wbs:
        print(f'{station}')
        for year in wbs[station]:
            if year == 'five_year':
                continue
            print(f'{year} -> '
                  f'V_E_max = {round(wbs[station][year]["full_year"].v_e_max, 2)}, '
                  f'most frequent = {round(wbs[station][year]["full_year"].most_frequent_wind_speed, 2)}, '
                  f'max power in one hour = {round(wbs[station][year]["full_year"].available_power_in_one_hour, 2)})')
            plot_weibull_pdf(wbs[station][year]['full_year'])

    print(' ')
    # Plot the average wind speeds for each station over the entire five year period
    wbs_to_plot = []
    for station in wbs:
        wbs_to_plot.append(wbs[station]['five_year'])
        print(f'{station} 2018-22 -> '
              f'Mean = {round(wbs[station]["five_year"].mean, 2)}, '
              f'Std = {round(wbs[station]["five_year"].std, 2)}, '
              f'P(X > Small turbine min) = {round(wbs[station]["five_year"].p_gt_small, 2)}, '
              f'P(X > Utility turbine min) = {round(wbs[station]["five_year"].p_gt_utility, 2)}')
    plot_weibull_mean_against_threshold(wbs_to_plot, 'All stations', '2018-22')

    print(' ')
    # Plot the average wind speeds for each station over the individual years
    for station in wbs:
        wbs_to_plot = []
        for year in wbs[station]:
            if year == 'five_year':
                continue
            wbs_to_plot.append(wbs[station][year]['full_year'])
            print(f'{station} {year} -> '
                  f'Mean = {round(wbs[station][year]["full_year"].mean, 2)}, '
                  f'Std = {round(wbs[station][year]["full_year"].std, 2)}, '
                  f'P(X > Small turbine min) = {round(wbs[station][year]["full_year"].p_gt_small, 2)}, '
                  f'P(X > Utility turbine min) = {round(wbs[station][year]["full_year"].p_gt_utility, 2)}')
        plot_weibull_mean_against_threshold(wbs_to_plot, station, '2018-22')

    # Plot the average wind speed for each station over the individual months
    for station in wbs:
        for year in wbs[station]:
            if year == 'five_year':
                continue
            print(f'\n\n{station} {year}')
            wbs_to_plot = []
            for month in wbs[station][year]:
                if month == 'full_year':
                    continue
                print(f'{wbs[station][year][month].name} = '
                      f'Mean: {round(wbs[station][year][month].mean, 2)}, '
                      f'Std: {round(wbs[station][year][month].std, 2)}, '
                      f'P(X > small turbine min): {round(wbs[station][year][month].p_gt_small, 2)}, '
                      f'P(X > utility turbine min): {round(wbs[station][year][month].p_gt_utility, 2)}')
                wbs_to_plot.append(wbs[station][year][month])
            plot_weibull_mean_against_threshold(wbs_to_plot, station, year)

    '''


if __name__ == '__main__':
    main()

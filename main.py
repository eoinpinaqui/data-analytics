# Local imports
from model import WeibullDistribution, plot_weibull_pdf, plot_weibull_cdfs
from data_processing import get_wind_speeds_for_years

([2018, 2020, 2022])


# The main function
def main():
    # Read in all of the data and plot the pdfs
    wbs = []
    places = ['Claremorris', 'Dunsany', 'Finner', 'Gurteen', 'Valentia']
    for idx, file in enumerate(
            ['./data/claremorris.csv', './data/dunsany.csv', './data/finner.csv', './data/gurteen.csv',
             './data/valentia.csv']):
        data = get_wind_speeds_for_years(file, [2018, 2020, 2022])

        for year in data:
            wbs.append(WeibullDistribution(f'{places[idx]} {year}', data[year]))
            plot_weibull_pdf(wbs[-1])

    # Example of plotting cdfs
    to_plot = []
    for wb in wbs:
        if '2018' in wb.name:
            to_plot.append(wb)

    plot_weibull_cdfs(to_plot)


if __name__ == '__main__':
    main()

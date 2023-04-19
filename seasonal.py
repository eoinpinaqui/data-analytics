# Local imports
from data import get_seasonal_wind_speeds_for_year

# Library imports
import scipy.stats
import matplotlib.pyplot as plt
import numpy as np

# Some useful constants
DISTRIBUTION_MAX = 30


# Get estimated weibull parameters
def fit_weibull(data: list):
    dist = scipy.stats.weibull_min
    params = dist.fit(data, floc=0)
    print(f'Weibull params: {params}')
    return params


# Plot the pdf of the distribution alongside a histogram
def plot_weibull_pdf(data, params, title=''):
    dist = scipy.stats.weibull_min
    x = [i for i in range(DISTRIBUTION_MAX)]
    pdf = dist.pdf(x, params[0], params[1], params[2])
    plt.plot(x, pdf, label='PDF')
    plt.hist(data, bins=DISTRIBUTION_MAX, density=True, label='Original data')
    plt.title(title)
    plt.legend()
    plt.xlabel('Probability')
    plt.ylabel('Wind speed (kts)')
    plt.show()


# Plot the cdf of the distribution alongside the cdf
def plot_weibull_cdf(params, year, place):
    dist = scipy.stats.weibull_min
    x = [i for i in range(DISTRIBUTION_MAX)]
    for season, p in params.items():
        cdf = dist.cdf(x, p[0], p[1], p[2])
        plt.plot(x, cdf, label=f'{season}')

    plt.title(f'CDF of fitted weibull distributions ({place} {year})')
    plt.legend()
    plt.xlabel('Probability')
    plt.ylabel('Wind speed (kts)')
    plt.show()


# The main function
def main():
    places = ['Claremorris', 'Dunsany', 'Finner', 'Gurteen', 'Valentia']
    for idx, file in enumerate(
            ['./data/claremorris.csv', './data/dunsany.csv', './data/finner.csv', './data/gurteen.csv',
             './data/valentia.csv']):
        data = get_seasonal_wind_speeds_for_year(file, [2018, 2020, 2022])

        for year, seasons in data.items():
            params = {}
            for season, wind_speeds in seasons.items():
                params[season] = np.array(fit_weibull(data[year][season]))
                plot_weibull_pdf(data[year][season], params[season],
                                 title=f'PDF of fitted weibull distribution ({places[idx]} {season} {year})')
            plot_weibull_cdf(params, year, places[idx])


if __name__ == '__main__':
    main()

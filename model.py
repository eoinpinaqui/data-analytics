# Library imports
import scipy.stats
import matplotlib.pyplot as plt
import numpy as np

# Recommended annual average wind speeds
SMALL_TURBINE = 7.77538
UTILITY_SCALE_TURBINE = 11.2743


# Class for holding all information about a weibull distribution
class WeibullDistribution:
    def __init__(self, name: str, data: list):
        self.name = name
        self.data = data

        # Fit the distribution (starts at 0 as negative wind speeds do not exist)
        self.params = scipy.stats.weibull_min.fit(self.data, floc=0)
        c, loc, scale = self.params

        # Get the mean and std of the distribution
        self.sample_mean = np.mean(data)
        self.sample_std = np.std(data)
        self.mean = scipy.stats.weibull_min.mean(self.params[0], self.params[1], self.params[2])
        self.std = scipy.stats.weibull_min.std(self.params[0], self.params[1], self.params[2])

        # Get the probability that the wind speed is greater than the thresholds
        self.p_gt_small = 1 - scipy.stats.weibull_min.cdf(SMALL_TURBINE, self.params[0], self.params[1], self.params[2])
        self.p_gt_utility = 1 - scipy.stats.weibull_min.cdf(UTILITY_SCALE_TURBINE, self.params[0], self.params[1], self.params[2])

        # Get the velocity that produces the maximum energy of the wind regime
        k = self.params[0]
        c = self.params[2]
        self.v_e_max = (c * (k + 2) ** (1 / k)) / k ** (1 / k)
        self.most_frequent_wind_speed = c * ((k - 1) / k) ** (1 / k)
        self.available_power_in_one_hour = (1.225 / 2) * (self.v_e_max / 1.943844) ** 3

        # Check the validity of the distribution (doesn't work on large data sets)
        self.ks = scipy.stats.kstest(self.data, scipy.stats.weibull_min.rvs(c, loc=loc, scale=scale, size=len(data)))


# Plot the means for a list of weibull distributions against recommended thresholds
def plot_weibull_mean_against_threshold(wbs: list, station: str, year: str):
    xs = [wb.name for wb in wbs]
    means = [wb.mean for wb in wbs]
    stds = [wb.std for wb in wbs]

    fig = plt.figure(figsize=(10, 6))
    plt.errorbar(xs, means, yerr=stds, fmt='o', color='blue', capsize=5,
                 label='Mean and standard deviation of wind speed')
    plt.axhline(SMALL_TURBINE, color='red', ls='dotted', label='Small turbine minimum')
    plt.axhline(UTILITY_SCALE_TURBINE, color='green', ls='dotted',
                label='Utility-scale turbine minimum')
    plt.title(f'Mean and standard deviation of fitted weibull distributions ({station}, {year})')
    if station == 'All stations':
        plt.xlabel('Station')
    elif year == '2018-22':
        plt.xlabel('Year')
    else:
        plt.xlabel('Month')
    plt.ylabel('Wind speed (kts)')
    plt.legend()
    plt.savefig(f'./plots/means/{station}/{year}.png')
    plt.close()


# Plot the mean wind speed and max energy wind speed
def plot_mean_and_max_energy_wind_speeds(wbs: list, station: str, year: str):
    xs = [wb.name for wb in wbs]
    means = [wb.mean for wb in wbs]
    frequents = [wb.most_frequent_wind_speed for wb in wbs]
    ve_maxs = [wb.v_e_max for wb in wbs]

    fig = plt.figure(figsize=(10, 6))
    plt.plot(xs, means, label='Mean wind speed')
    plt.plot(xs, frequents, label='Most frequent wind speed')
    plt.plot(xs, ve_maxs, label='Wind speed contributing to maximum energy')
    plt.title(f'Wind speed potential ({station}, {year})')
    if station == 'All stations':
        plt.xlabel('Station')
    elif year == '2018-22':
        plt.xlabel('Year')
    else:
        plt.xlabel('Month')
    plt.ylabel('Wind speed (kts)')
    plt.legend()
    plt.savefig(f'./plots/densities/{station}/{year}.png')
    plt.close()


# Plot the pdf for a weibull distribution
def plot_weibull_pdf(wb: WeibullDistribution, station: str, year: str, month: str):
    max_wind_speed = int(max(wb.data))
    x = [i for i in range(max_wind_speed)]
    pdf = scipy.stats.weibull_min.pdf(x, wb.params[0], wb.params[1], wb.params[2])

    fig = plt.figure(figsize=(10, 6))
    plt.plot(x, pdf, label='PDF')
    plt.hist(wb.data, bins=max_wind_speed, density=True, label='Sample data')
    plt.title(f'PDF for {station} ({year} {month})')
    plt.legend(loc='lower left')
    plt.xlabel('Wind speed (kts)')
    plt.ylabel('Probability')
    if year == '':
        year = '2018-22'
        month = 'five years'
    elif month == '':
        month = 'full year'
    plt.savefig(f'./plots/pdfs/{station}/{year}/{month}.png')
    plt.close()


# Plot the cdfs for a list of weibull distributions
def plot_weibull_cdfs(wbs: list):
    for wb in wbs:
        x = [i for i in range(50)]
        cdf = scipy.stats.weibull_min.cdf(x, wb.params[0], wb.params[1], wb.params[2])
        plt.plot(x, cdf, label=wb.name)

    plt.title('CDFs of fitted weibull distributions')
    plt.legend()
    plt.xlabel('Wind speed (kts)')
    plt.ylabel('Probability')
    plt.show()

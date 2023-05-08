# Library imports
import scipy.stats
from functools import partial
import matplotlib.pyplot as plt

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
        self.mean = scipy.stats.weibull_min.mean(self.params[0], self.params[1], self.params[2])
        self.std = scipy.stats.weibull_min.std(self.params[0], self.params[1], self.params[2])

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
    plt.axhline(SMALL_TURBINE, color='red', ls='dotted', label='Recommended annual minimum (small turbine)')
    plt.axhline(UTILITY_SCALE_TURBINE, color='green', ls='dotted',
                label='Recommended annual minimum (utility-scale turbine)')
    plt.title(f'Mean and standard deviation of fitted weibull distributions ({station}, {year})')
    plt.xlabel('Time period')
    plt.ylabel('Average wind speed (kts)')
    plt.legend()
    plt.show()


# Plot the pdf for a weibull distribution
def plot_weibull_pdf(wb: WeibullDistribution):
    max_wind_speed = max(wb.data)
    x = [i for i in range(max_wind_speed)]
    pdf = scipy.stats.weibull_min.pdf(x, wb.params[0], wb.params[1], wb.params[2])
    plt.plot(x, pdf, label='PDF')
    plt.hist(wb.data, bins=max_wind_speed, density=True, label='Sample data')
    plt.title(f'PDF of {wb.name}')
    plt.legend(loc='lower left')
    plt.xlabel('Wind speed (kts)')
    plt.ylabel('Probability')
    plt.show()


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

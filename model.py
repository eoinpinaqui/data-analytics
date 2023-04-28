# Library imports
import scipy.stats
from functools import partial
import matplotlib.pyplot as plt


# Class for holding all information about a weibull distribution
class WeibullDistribution:
    def __init__(self, name: str, data: list):
        self.name = name
        self.data = data

        # Fit the distribution (starts at 0 as negative wind speeds do not exist)
        self.params = scipy.stats.weibull_min.fit(self.data, floc=0)
        c, loc, scale = self.params

        # Check the validity of the distribution
        self.ks = scipy.stats.kstest(self.data, scipy.stats.weibull_min.rvs(c, loc=loc, scale=scale, size=len(data)))

        # Print some info about the fitted distribution
        print(f'{self.name}: Weibull parameters: {self.params}, KS test: {self.ks}')


# Plot the pdf for a weibull distribution
def plot_weibull_pdf(wb: WeibullDistribution):
    max_wind_speed = max(wb.data)
    x = [i for i in range(max_wind_speed)]
    pdf = scipy.stats.weibull_min.pdf(x, wb.params[0], wb.params[1], wb.params[2])
    plt.plot(x, pdf, label='PDF')
    plt.hist(wb.data, bins=max_wind_speed, density=True, label='Sample data')
    plt.title(f'PDF of {wb.name}')
    plt.legend()
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

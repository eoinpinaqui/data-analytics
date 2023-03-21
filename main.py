# Library imports
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats


# Read data in from a csv file
def get_windspeeds(file):
    data = pd.read_csv(file)
    wind_data = data['wdsp'].tolist()

    windspeeds = []

    for speed in wind_data:
        if type(speed) is int or type(speed) is float:
            windspeeds.append(int(speed))

    return windspeeds


windspeeds = get_windspeeds('./data/mayo.csv')

# Fit the distribution
dist = scipy.stats.weibull_min
params = dist.fit(windspeeds)
print(f'Weibull params: {params}')

# Plot the pdf of the distribution alongside a historgram
x = [i for i in range(50)]
pdf = dist.pdf(x, params[0], params[1], params[2])
plt.plot(x, pdf)
plt.hist(windspeeds, bins=50, density=True)
plt.show()



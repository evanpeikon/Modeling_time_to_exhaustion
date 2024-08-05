# import libraries
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# create data frame to store deoxy - duration data
data = pd.DataFrame({
    'De-oxy rate': [-0.019, -0.035, -0.048, -0.068, -0.22], 
    'Duration': [7200, 4800, 3600, 2400, 1200]})

# define function for critical metabolic rate model
def critical_metabolic_rate(t, CMR, M_prime):
    return CMR + M_prime / t

# extract deoxy rate and duration data from data frame
deoxy_rate = data['De-oxy rate'].values
duration = data['Duration'].values

# perform non-linear regression to fit the deoxy rate - duration model 
popt, pcov = curve_fit(critical_metabolic_rate, duration, deoxy_rate)
CMR, M_prime = popt

# print the estimated parameters
print(f"Estimated Critical Metabolic Rate (CMR): {CMR:.5f} %/s")
print(f"Estimated M': {M_prime:.5f}")

# plot the data and the fitted model
plt.scatter(duration, deoxy_rate, label='Athlete Data', color='blue')
t_fit = np.linspace(min(duration), max(duration), 100)
P_fit = critical_metabolic_rate(t_fit, CMR, M_prime)
plt.plot(t_fit, P_fit, label='Fitted Model', color='red')
plt.xlabel('Duration (seconds)')
plt.ylabel('Deoxygenation Rate (%/s)')
plt.legend()
plt.show()

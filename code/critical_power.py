# import libraries
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Create data frame to store power - duration data
data = pd.DataFrame({
    'Power (watts)': [278, 349, 435, 465,  725], 
    'Duration (sec)': [3533, 1790, 600, 300, 120]})

# define function for power duration curve
def power_duration_curve(t, CP, W_prime):
  power = CP + W_prime / t
  return power

# extract power and duration data from data frame 
power = data['Power (watts)'].values
duration = data['Duration (sec)'].values

# perform non-linear regression to fit the power - duration model 
popt, pcov = curve_fit(power_duration_curve, duration, power)
CP, W_prime = popt

# print the estimated parameters
print(f"Estimated Critical Power (CP): {CP:.1f} Watts")
print(f"Estimated W': {W_prime:.1f} Joules")

plt.scatter(duration, power, label='Athlete data', color='blue')
t_fit = np.linspace(min(duration), max(duration), 100)
P_fit = power_duration_curve(t_fit, CP, W_prime)
plt.plot(t_fit, P_fit, label='Fitted Model', color='red')
plt.xlabel('Duration (seconds)')
plt.ylabel('Power (watts)')
plt.legend()
plt.show()

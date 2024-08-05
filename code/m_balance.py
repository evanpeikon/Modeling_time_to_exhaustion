# import libraries
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

filename = 'O2.csv'
names = ['time', 'SmO2', 'SmO2_accel', 'SmO2_jerk', 'acceleration','jerk']
workout_data = pd.read_csv(filename, names=names)

# Define a rolling window size
window_size = 10

# calculate rolling metrics
workout_data['SmO2_rolling_mean'] = workout_data['SmO2'].rolling(window=window_size).mean()
workout_data['SmO2_accel_rolling_mean'] = workout_data['SmO2_accel'].rolling(window=window_size).mean()
workout_data = workout_data.fillna(method='bfill')

# set CMR and M' varialbes
# If you didn't run the critical_metabolic_rate.py script prior, you'll need to manually input CMR and M_prime values here
CMR = CMR
M_prime = M_prime * - 1 # Invert sign

# initialize M' balance model
M_bal = np.zeros(len(workout_data))
M_bal[0] = M_prime
tau_recovery = 300  # Example recovery time constant, adjust as needed

# update M' balance
for i in range(1, len(workout_data)):
    dt = workout_data['time'].iloc[i] - workout_data['time'].iloc[i - 1]
    d_rate = workout_data['SmO2_accel_rolling_mean'].iloc[i]
    if d_rate < CMR: # Depletion of M'
        M_bal[i] = M_bal[i - 1] - (CMR - d_rate) * dt
    else: # restoration of M'
        M_bal[i] = M_bal[i - 1] + (M_prime - M_bal[i - 1]) * (1 - np.exp(-dt / tau_recovery))

    # Ensure M' balance does not go below 0 or above M'

# add M' balance to workout data
workout_data['M_bal'] = M_bal

# create subplots
fig, ax1 = plt.subplots(figsize=(10, 6))

# plot M' Balance on the left y-axis
ax1.plot(workout_data['time'], workout_data['M_bal'], label="M' Balance", color='red')
ax1.set_xlabel('Time (seconds)')
ax1.set_ylabel("M' Balance", color='red')
ax1.tick_params(axis='y', labelcolor='red')

# create a second y-axis to plot SmO2
ax2 = ax1.twinx()
ax2.plot(workout_data['time'], workout_data['SmO2'], label='Δ SmO2 Rate', color='blue')
ax2.set_ylabel('Muscle oxygenation (%)', color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

# add legends and show plot
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc='best')
plt.show()

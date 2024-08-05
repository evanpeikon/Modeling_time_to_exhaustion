# import libraries 
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# set CP and W' varialbes
CP = CP # If you didn't run the critical_power.py script prior, you'll need to manually input CP and W_prime values here
W_prime = W_prime # If you didn't run the critical_power.py script prior, you'll need to manually input CP and W_prime values here

# Load the CSV file
filename = 'power2.csv'
names = ['time', 'power']
workout_data = pd.read_csv(filename, names=names)
workout_data = workout_data.dropna()
workout_data.reset_index(drop=True, inplace=True)

# Initialize W' balance
W_bal = np.zeros(len(workout_data))
W_bal[0] = W_prime

# Time constant for W' recovery (in seconds)
tau_recovery = 300  # Example recovery time constant, adjust as needed

# Function to update W' balance
for i in range(1, len(workout_data)):
    dt = workout_data['time'].iloc[i] - workout_data['time'].iloc[i - 1]
    power = workout_data['power'].iloc[i]

    if power > CP:
        # Depletion of W'
        W_bal[i] = W_bal[i - 1] - (power - CP) * dt
    else:
        # Recovery of W'
        W_bal[i] = W_bal[i - 1] + (W_prime - W_bal[i - 1]) * (1 - np.exp(-dt / tau_recovery))

    # Ensure W' balance does not go below 0 or above W'
    W_bal[i] = max(0, min(W_prime, W_bal[i]))

# Add W' balance to workout data
workout_data['W_bal'] = W_bal

# Plot the results
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot W' Balance on the left y-axis
ax1.plot(workout_data['time'], workout_data['W_bal'], label="W' Balance", color='red')
ax1.set_xlabel('Time (seconds)')
ax1.set_ylabel("W' Balance (Joules)", color='red')
ax1.tick_params(axis='y', labelcolor='red')

# Create a second y-axis to plot Power Output
ax2 = ax1.twinx()
ax2.plot(workout_data['time'], workout_data['power'], label='Power Output', color='blue')
ax2.set_ylabel('Power Output (Watts)', color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

# Combine legends from both y-axes
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc='best')

# Show the plot
plt.show()

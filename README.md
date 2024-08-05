# What Is Critical Power?
Critical power is mathematically defined as the power-asymptote of the hyperbolic relationship between power output and time to exhaustion. In essence, critical power describes the duration that an individual can sustain a fixed power output in the severe exercise intensity domain, and physiologically critical power represents the boundary between steady-state and non-steady-state exercise]. As a result, critical power may provide a more meaningful fitness index over more well-known performance metrics such as VO2max or functional threshold power. The hyperbolic equation which describes the relationship between power output and exercise tolerance within the severe exercise intensity domain is as follows:

```
Time to Exhaustion = W’ / Power - Critical Power
```

This equation creates a two-parameter model where critical power represents the asymptote for power, and the W’ represents a finite amount of work that can be done above critical power]. Taken together, these two parameters can be used to predict how long an individual can exercise at any intensity above their critical power output. Interestingly, the critical power model appears to apply across kingdoms, phylums,  and classes of animal life as well as different forms of exercise, and individual muscles for a given athlete. These observations suggest a highly conserved and organized physiological process, and perhaps a unifying principle of bioenergetics.

# How Is Critical Power Calculated?
There are currently two validated methods for determining critical power and the fixed amount of work that can be done above critical power, termed W’. Traditionally critical power and W’ were calculated after having an individual perform three to seven all-out work bouts where they hold a fixed power-output until failure. These test results are then plotted on a chart where the x,y variables represent time to failure and power for each trial. Critical power is then determined as the slope of the work-time relationship, whereas W’ is determined from the y-intercept. More recently, though, investigators have introduced a 3-minute all-out exercise test, known as the 3MT, that has enabled the determination of critical power and W’ from a single exercise bout. The idea behind the 3-minute all-out test is that when a subject exerts themselves fully and expends W’ wholly, their finishing power output equals their critical power. 

In the code block below, I'll show you how to calcualte critical power using an athlete's historic training data from multiple time to exhaustion trials:

```python
# import libraries 
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Create data frame to store power - duration data
data = pd.DataFrame({
    'Power (watts)': [278, 349, 455, 435,  725], 
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

# print the estimated CP and W' values
print(f"Estimated Critical Power (CP): {CP:.1f} Watts")
print(f"Estimated W': {W_prime:.1f} Joules")
```
Which, produces the following output:
- Estimated Critical Power (CP): 306.8 Watts
- Estimated W': 50664.4 Joules

After calculating critical power with the code block above, we can plot the athlete's power-duration curve using the following code:

```python
plt.scatter(duration, power, label='Athlete data', color='blue')
t_fit = np.linspace(min(duration), max(duration), 100)
P_fit = power_duration_curve(t_fit, CP, W_prime)
plt.plot(t_fit, P_fit, label='Fitted Model', color='red')
plt.xlabel('Duration (seconds)')
plt.ylabel('Power (watts)')
plt.legend()
plt.show()
```







# libraries
import matplotlib.pyplot as plt
import numpy as np



x_values = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
y1 = [92.00,75.50,58.49,48.88,45.20,42.73,39.64,35.65,24.03]
y2 = [92.87,80.80,68.69,61.25,54.52,50.99,45.77,39.18,26.87]

y3 = [92.1,79.85,70.30,61.23,55.24,52.67,47.83,41.48,33.09]
y4 = [91.90,81.55,69.27,61.85,56.48,51.42,46.5,38.65,26.48]


plt.plot(x_values,y1, label = 'Basic Agent',marker = 'o')
plt.plot(x_values,y2, label = 'Improved Agent',marker = 'o')
plt.plot(x_values,y3, label = 'Global Improved Agent',marker = 'o')
plt.plot(x_values,y4, label = 'Better Improved Agent',marker = 'o')


plt.xlabel('Mine Density')
plt.ylabel('Total Score As % (Mines Identified / Total Mines)')
plt.legend()
plt.get_current_fig_manager().canvas.set_window_title('Performance')
plt.title('Improved Agent Global and Better Improved Agent')


# show graph
plt.show()









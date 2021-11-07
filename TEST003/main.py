import pandas as pd

import matplotlib.pyplot as plot

 

growthData = {"Countries": ["Country1", "Country2", "Country3", "Country4", "Country5", "Country6", "Country7"],

              "Growth Rate":[10.2, 7.5, 3.7, 2.1, 1.5, -1.7, -2.3]}

dataFrame  = pd.DataFrame(data = growthData)

dataFrame.plot.barh(x='Countries', y='Growth Rate', title="Growth rate of different countries")

plot.show(block=True)

growthData = {"Stock": ["0056", "2330", "0050"],

              "Growth Rate":[0.4846, 0.2973, -0.2219]}

dataFrame  = pd.DataFrame(data = growthData)

dataFrame.plot.barh(x='Stock', y='Growth Rate', title="Growth rate of different countries")

plot.show(block=True)

Stock = ["0056", "2330", "0050"]
Growth = [0.4846, 0.2973, -0.2219]
plot.bar(Stock, Growth, 0.5)
plot.show()
import math


rmse = lambda actual, expected: math.sqrt(((actual - expected)**2).mean())

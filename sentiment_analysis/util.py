import math
from matplotlib import (mlab, pyplot as plt)
from IPython.display import display, Markdown

rmse = lambda actual, expected: math.sqrt(((actual - expected)**2).mean())

green = '#008f41'

def plot_results(actual, expected):
    display(Markdown("### RMSE: %.5f" % rmse(actual, expected)))
    plt.title('Predicted (green) vs Desired (red)')
    plt.ylabel('Accuracy')
    plt.xlabel('Rating')
    plt.scatter(actual, expected, color=green, alpha=0.5)
    plt.plot([0, 10], [0, 10], color='red')
    plt.show()
    plt.title('Predicted (red) vs Actual (green)')
    plt.ylabel('Review Count')
    plt.xlabel('Rating')
    plt.hist(actual, 40, facecolor=green)
    plt.hist(expected, 40, facecolor='red', alpha=0.5)
    plt.show()
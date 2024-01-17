#!/usr/bin/python3
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
import matplotlib as mpl
import matplotlib.colors as mc
from plots import plot_line, set_fonts

# USAGE: python sampleplot.py sample.data

mu=10
lam=10
ts=0.1
delta=0.1
def theoretical(x):
    # return x*1.05+0.11
    return (1-x)*(delta+1/mu) + x*(1/(mu - lam*x))
    

if __name__ == "__main__":
    # set_fonts()  # NON USARE SE NON SI HA LATEX INSTALLATO
    # plot respone time
    fig, ax = plt.subplots()
    ax.set(xlabel='$x$', ylabel='Time [s]')
    plot_line(ax, 'o--', 'sample.data', 'Response Time', '#x', 'y', 'sigma(y)')
    pts=[x/10.0 for x in range(1, 10)]
    plot_line(ax, '-', None, 'Theoretical Curve', pts, [theoretical(x) for x in pts])
    plt.legend()
    plt.savefig('sample.png')
    plt.show()


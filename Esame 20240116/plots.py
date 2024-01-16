#!/usr/bin/python3
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
import matplotlib as mpl
import matplotlib.colors as mc
#import pathlib

def set_fonts():
    """ 
    Set LaTeX-friendly fonts. Call this function at the beginning of your code
    """
    mpl.rcParams['font.family'] = 'Nimbus Sans'
    mpl.rcParams["figure.autolayout"] = True
    mpl.rc('text', usetex=True)
    mpl.rcParams.update({'font.size': 10})

def plot_line(ax, format, fname, label, xcol, ycol, errcol=None):
    """
    Plot a line from data
    
    Parameters
    ----------
    ax : 
        canvas for plotting. Refer to matplotlib.pyplot. Can ge the object returned by matplotlib.pyplot.subplots()
    format: str
        format string. Refer to matplotlib.pyplot
    fname: str or None
        name of a tab-separated column file. Column names are on the first row
    label: str
        label of the curve in the plot
    xcol:
        the x data for the plot 
        can be the name of a column in a dataframe if fname is a file with data
        can be a callable that is invoked on the dataframe
        can be a set list/array with data
    ycol:
        like xcol, but this is the y data of the plot
    errcol:
        like xcol but ti can aslo be none. If set it contains the error values to represent a confidence interval
    """
    if fname is not None:
        data = pd.read_csv(fname, sep='\t')
    use_data=fname is not None and not callable(xcol) and not callable(ycol) and not callable(errcol)
    xcol = xcol(data) if callable(xcol) else xcol
    ycol = ycol(data) if callable(ycol) else ycol
    errcol=errcol(data) if callable(errcol) else errcol
    data=data if use_data else None
    if errcol is not None:
        ax.errorbar(xcol, ycol, yerr=errcol, data=data, fmt=format, label=label, capsize=5)
    else:
        ax.plot(xcol, ycol, format, data=data, label=label)


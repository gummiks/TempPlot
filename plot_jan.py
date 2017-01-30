#!/usr/bin/python
# -*- coding: utf-8 -*-
# File: thermal_encl_temps.py
# Created: 2014-11-14 by gks 
"""
Description: A script to plot the temp data
"""
import sys
from pylab import *
from scipy import *
import helper_funcs as hf
reload(hf)

total_save_name = "LakeShoreLogTotal.txt"
summary_name = "LakeShoreLogSummary.txt"

# Create the total dataset (LakeShoreLogTotal.txt)
hf.create_total_dataset("archive/",total_save_name,summary_name)

# Misc plotting settings
hf.config_matplotlib()

# Plot whole dataset from Jan 10 2015 to today
hf.plot_all_dataset_jan(total_save_name)

hf.plot_today(total_save_name)

hf.plot_week(total_save_name)

hf.plot_month(total_save_name)

# A function to plot specific dates
#helper_funcs.plot_dates(total_save_name,'2014-11-15','2014-11-16')

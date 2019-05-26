# -*- coding: utf-8 -*-
"""
Created on Mon May 20 20:26:36 2019

@author: Diego
"""


import pandas as pd
import matplotlib.pyplot as plt


if __name__ == "__main__":
    
    csv_file = pd.read_csv("../preprocessed_data/csv_eye.csv", sep = ";", header = 0)
    #plot the top 10 eyes with the most elevated cornea
    csv_file[['Max Depth Front', 'Max Depth Back']].sort_values(by = ['Max Depth Front', 'Max Depth Back'], ascending = True)\
                                                    .head(10)\
                                                    .plot(kind = 'barh', title = 'Top 10 Max Depth')
    
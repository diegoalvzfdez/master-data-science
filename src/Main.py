# -*- coding: utf-8 -*-
"""
Created on Sat May 18 11:35:22 2019

@author: Diego Álvarez Fernández
"""

import pandas as pd
from managecsv import manage_csv
import tkinter as tk
from tkinter import filedialog


if __name__ == "__main__":
    a='S'
    x = []
    y = []
    while a == 'S':
        root = tk.Tk()
        root.withdraw()
    
        file_path1 = filedialog.askopenfilename()
        file_path2 = filedialog.askopenfilename()
        file_path3 = filedialog.askopenfilename()
        csv_object = manage_csv(file_path1, file_path2, file_path3)
    
        x.append(csv_object.x)
        y.append("")
        a = 'n'
    #creamos un fichero para almacenar los datos obtenidos para acciones posteriores   
    csv_file = pd.DataFrame(x, columns = ['Max Depth Front', 
                                          'Max Depth Back', 
                                          'Max Curve Front', 
                                          'Max Curve Back', 
                                          'Max Variation Curve Front', 
                                          'Max Variation Curve Back', 
                                          'Mean Curve Front', 
                                          'Mean Curve Back', 
                                          'Age', 
                                          'K Max', 
                                          'Paqui Min', 
                                          'Distance Between Max Curve and Min Paqui'])
    
    csv_file_y = pd.DataFrame(y, columns = ['Treatment'])
    
    csv_file['Treatment'] = csv_file_y
    
    #redondeamos a dos decimales aquellos valores que sean de tipo float para que no den problemas al exportarlos a un archivo csv
    csv_file['Mean Curve Front'] = csv_file['Mean Curve Front'].map(lambda x: round(x, 2))
    csv_file['Mean Curve Back'] = csv_file['Mean Curve Back'].map(lambda x: round(x, 2))
    csv_file['Distance Between Max Curve and Min Paqui'] = csv_file['Distance Between Max Curve and Min Paqui'].map(lambda x: round(x, 2))
    csv_file['Max Curve Front'] = csv_file['Max Curve Front'].map(lambda x: round(x, 2))
    csv_file['Max Curve Back'] = csv_file['Max Curve Back'].map(lambda x: round(x, 2))
    csv_file['Max Variation Curve Front'] = csv_file['Max Variation Curve Front'].map(lambda x: round(x, 2))
    csv_file['Max Variation Curve Back'] = csv_file['Max Variation Curve Back'].map(lambda x: round(x, 2))
    csv_file['K Max'] = csv_file['K Max'].map(lambda x: round(x, 2))
    
    csv_file.to_csv("../data/csv_eye.csv", sep = ";", index = False)
# -*- coding: utf-8 -*-
"""
Created on Sat May 18 11:35:22 2019

@author: Diego Álvarez Fernández
"""

import pandas as pd
from managecsv import manage_csv
from os import listdir
from os.path import isfile, join

if __name__ == "__main__":
    x = []
    y = []
    data_path = 'C:/Users/lique/OneDrive/Documents/GitHub/master-data-science/data'
    #obtenemos los ficheros necesarios para realizar la ETL
    datafiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]
    #ordenamos alfabéticamente el string para evitar errores
    datafiles.sort()
    
    #necesitamos tener los ficheros agrupados de tres en tres, por lo que necesitamos crear una lista de listas
    files_virtual = []
    files_final = []
    i_comp = 0
    
    for i in range(len(datafiles)):
        #sumamos 1 para poder hacer las agrupaciones de 3 en 3
        i_comp = i + 1
        if i_comp%3 != 0:
            files_virtual.append(datafiles[i])
        elif i_comp%3 == 0:
            files_virtual.append(datafiles[i])
            files_final.append(files_virtual)
            files_virtual = []
            
    for i in range(len(files_final)):
        #al haber ordenado anteriormente el string alfabéticamente, sabemos que el fichero de curvatura es el primero, el de elevación el segundo y el de paquimetría el tercero
        stop = files_final[i]
        file_ele = data_path + "/" + files_final[i][1]
        file_curv = data_path + "/" + files_final[i][0]
        file_paqui = data_path + "/" + files_final[i][2]
        #se dan casos en los cuales los ficheros vienen corruptos, por lo que en el caso de no poder realizar las operaciones, pasamos a la siguiente iteración
        try:
            csv_object = manage_csv(file_ele, file_curv, file_paqui)
        except:
            continue
        x.append(csv_object.x)
        y.append("1")
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
                                          'Distance Between Max Curve and Min Paqui',
                                          'Position of Most Curve Point Relative to Center'])
    
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
    csv_file['Position of Most Curve Point Relative to Center'] = csv_file['Position of Most Curve Point Relative to Center'].map(lambda x: round(x, 2))
    
    csv_file.to_csv("../preprocessed_data/csv_eye.csv", sep = ";", index = False)
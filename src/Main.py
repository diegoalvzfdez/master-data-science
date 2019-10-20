# -*- coding: utf-8 -*-
"""
Created on Sat May 18 11:35:22 2019

@author: Diego Álvarez Fernández
"""

import pandas as pd
from managecsv import manage_csv
from os import listdir
from os.path import isfile, join
from tkinter import filedialog
from tkinter import *
from tkinter import messagebox

#introducimos el tratamiento como una variable global para poder atacarla desde las funciones de tkinter
treatment = 1

def writeFile():
    answer = metinF.get()
    if answer == '1' or answer == '2' or answer == '3':
        global treatment
        treatment = metinF.get()
        pop_up_introduce_treatment.destroy()
        pop_up_introduce_treatment.quit()

if __name__ == "__main__":
    #creamos los vectores que van a determinar nuestro dataset final
    x = []
    y = []
    pacient_info = pd.DataFrame(columns = ['First Name', 'Last Name', 'Eye'])
    #generamos un diccionario que nos permite introducir la cadena de texto para definir el tratamiento
    dict_treatment = {'1': 'Pacientes sin operar',
                      '2': 'Pacientes tratados mediante crosslinking',
                      '3': 'Pacientes tratados mediante anillos'}
    continuar = 1
    while continuar == 1:
        
        root = Tk()
        root.withdraw()
        options = {}
        options['title'] = 'Seleccione donde se encuentran los ficheros'    
        #seleccionamos donde se encuentran los ficheros que queremos introducir
        data_path = filedialog.askdirectory(**options)
        #obtenemos los ficheros necesarios para realizar la ETL
        datafiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]
        #ordenamos alfabéticamente el string para evitar errores
        datafiles.sort()
        
        #introducimos el tratamiento de los pacientes
        pop_up_introduce_treatment = Tk()
        
        text = Label(pop_up_introduce_treatment, text="¿Los ficheros que está introduciendo pertenecen a (1) pacientes sin operar, (2) pacientes operados mediante crosslinking o (3) pacientes operados mediante anillos?")
        text.grid(row=7, column=1)
        
        metinF = Entry(pop_up_introduce_treatment)
        metinF.grid(row=8, column=1)
        
        butonWrite = Button(pop_up_introduce_treatment)
        butonWrite.config(text = 'Aceptar', command = writeFile)
        butonWrite.grid(row=9, column=1)
        
        pop_up_introduce_treatment.mainloop()
        
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
            y.append(dict_treatment[treatment])
            data_df = {'First Name': [0], 'Last Name': [0], 'Eye': [0]}
            virtual_df = pd.DataFrame(data = data_df)
            info = csv_object.pacient_info
            virtual_df['First Name'] = info[0]
            virtual_df['Last Name'] = info[1]
            virtual_df['Eye'] = info[2]
            pacient_info = pacient_info.append(virtual_df)
        pop_up_continue = messagebox.askquestion("Salir", "¿Desea continuar introduciendo datos?", icon='warning')
        if pop_up_continue == 'yes':
            continuar = 1
        else:
            continuar = 0
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
    
    #csv_file.to_csv("../preprocessed_data/csv_eye.csv", sep = ";", index = False)
    
    #comprobamos los datos que hemos obtenido de los pacientes

    csv_historical = pd.read_csv('../data/patient_data.csv', sep = ';')
    csv_export = csv_historical.append(pacient_info)
    csv_export = csv_export.drop_duplicates(['First Name', 'Last Name', 'Eye'], keep = 'first')
    csv_export.to_csv('../data/patient_data.csv', sep = ';')
    
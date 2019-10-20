# -*- coding: utf-8 -*-
"""
Created on Sat May 18 11:35:22 2019

@author: Diego Álvarez Fernández
"""

import pandas as pd
import datetime
import copy
import math

class manage_csv:
    
    df_curv_front_with_axis = pd.DataFrame()
    df_curv_back_with_axis = pd.DataFrame()
    df_paqui_with_axis = pd.DataFrame()
    df_ele = pd.DataFrame()
    df_curv = pd.DataFrame()
    df_paqui = pd.DataFrame()
    df_stacked_back = pd.DataFrame()
    df_stacked_front_ele = pd.DataFrame()
    df_stacked_front_cur = pd.DataFrame()
    df_stacked_back_ele = pd.DataFrame()
    df_stacked_back_cur = pd.DataFrame()
    max_depth_front = 0
    max_depth_back = 0
    max_curve_front = 0
    max_curve_back = 0
    min_curve_front = 0
    min_curve_back = 0
    var_curve_front = 0
    var_curve_back = 0
    mean_curve_front = 0
    mean_curve_back = 0
    age = 0
    first_name = ""
    last_name = ""
    eye = ""
    k_max = 0
    paqui_min = 0
    distance = 0
    x_cornea = 0
    y_cornea = 0
    max_curve_pos_rel_to_center = 0
    x = []
    pacient_info = []
    
    def stack_and_transform_front(self, df, status):
        
        #obtenemos el DataFrame necesario que contiene los datos de la parte anterior del ojo
        df_back = copy.deepcopy(df)
        df_back['ID'] = df_back.index
        df_back.reset_index(inplace = True)
        #los datos se encuentran entre el valor BACK y el valor BACK related to FRONT (en el caso del fichero de elevacion) o TANGENTIAL FRONT (en el caso del fichero de curvatura) contenidos en los indices
        id_back = df_back[df_back['ID'] == 'BACK'].index.values.astype(int)[0]
        if status == 1:
            id_tangential_front = df_back[df_back['ID'] == 'BACK related to FRONT'].index.values.astype(int)[0]
        if status == 2:
            id_tangential_front = df_back[df_back['ID'] == 'TANGENTIAL FRONT'].index.values.astype(int)[0]
        df_back = df_back.truncate(before = id_back + 1, after = id_tangential_front -1)
        df_back.drop('ID', axis = 1, inplace = True)
        df_back.set_index('FRONT', inplace = True)
        df_stacked_back = df_back.stack()
        df_stacked_back = df_stacked_back.reset_index()
        df_stacked_back = df_stacked_back.rename(index = str, columns = {'FRONT': 'X', 'level_1': 'Y', 0: 'Z'})
        
        #stackeamos los datos para poder tener los valores de Z en función de X e Y
        df_stacked_front = df.stack()
        df_stacked_front = df_stacked_front.reset_index()
        df_stacked_front = df_stacked_front.rename(index = str, columns = {'FRONT': 'X', 'level_1': 'Y', 0: 'Z'})
        #Creamos una nueva columna donde introducimos los valores de los ID para poder hacer transformaciones posteriores
        df_stacked_front['ID'] = df_stacked_front.index
        df_stacked_front['ID'] = pd.to_numeric(df_stacked_front['ID'])
        
        if status == 1:
            self.df_stacked_front_ele = df_stacked_front[df_stacked_front['ID'] < list(df_stacked_front[df_stacked_front['X'] == 'BACK']['ID'])[0]]
            self.df_stacked_front_ele.drop(['X', 'Y', 'ID'], axis = 1, inplace = True)
            self.df_stacked_back_ele = df_stacked_back
            self.df_stacked_back_ele.drop(['X', 'Y'], axis = 1, inplace = True)
            
        if status == 2:
            self.df_stacked_front_cur = df_stacked_front[df_stacked_front['ID'] < list(df_stacked_front[df_stacked_front['X'] == 'BACK']['ID'])[0]]
            self.df_curv_front_with_axis =  copy.deepcopy(self.df_stacked_front_cur.drop(['ID'], axis = 1))
            self.df_stacked_front_cur.drop(['X', 'Y', 'ID'], axis = 1, inplace = True)
            self.df_stacked_back_cur = df_stacked_back
            self.df_curv_back_with_axis = copy.deepcopy(df_stacked_back)
            self.df_stacked_back_cur.drop(['X', 'Y'], axis = 1, inplace = True)

    def stack_and_get_axis(self, df_paqui):
        
        df_stacked_paqui = df_paqui.stack()
        df_stacked_paqui = df_stacked_paqui.reset_index()
        df_stacked_paqui = df_stacked_paqui.rename(index = str, columns = {'level_0': 'X', 'level_1': 'Y', 0: 'Z'})
        #Creamos una nueva columna donde introducimos los valores de los ID para poder hacer transformaciones posteriores
        df_stacked_paqui['ID'] = df_stacked_paqui.index
        df_stacked_paqui['ID'] = pd.to_numeric(df_stacked_paqui['ID'])
        self.df_paqui_with_axis = df_stacked_paqui
        self.df_paqui_with_axis = df_stacked_paqui[df_stacked_paqui['ID'] < list(df_stacked_paqui[df_stacked_paqui['X'] == 'Name']['ID'])[0]]
        self.df_paqui_with_axis.drop(['ID'], axis = 1, inplace = True)
        

    def get_max_distance(self):
        
        #necesitamos conocer el punto de mayor curvatura, pudiendo ser de la parte posterior como de la parte anterior
        axis_front = self.df_curv_front_with_axis.sort_values(by = ['Z'], ascending = True).head(1)
        axis_back = self.df_curv_back_with_axis.sort_values(by = ['Z'], ascending = True).head(1)
        if axis_front['Z'][0] < axis_back['Z'][0]:
            axis_final = axis_front
        else:
            axis_final = axis_back       
        #obtenemos el valor de las coordenadas del punto con mayor curvatura
        max_axis_curv = axis_final.drop(['Z'], axis = 1).values.tolist()
        axis_paqui = self.df_paqui_with_axis.sort_values(by = ['Z'], ascending = True).drop(['Z'], axis = 1).head(1).values.tolist()
        self.distance = math.sqrt(((float(max_axis_curv[0][0].replace(",", ".")) - float(axis_paqui[0][0].replace(",", ".")))**2)+((float(max_axis_curv[0][1].replace(",", ".")) - float(axis_paqui[0][1].replace(",", ".")))**2))
        self.max_curve_pos_rel_to_center = math.sqrt(((float(max_axis_curv[0][0].replace(",", ".")) - self.x_cornea)**2)+((float(max_axis_curv[0][1].replace(",", ".")) - self.y_cornea)**2))
        
        
        
    def get_max_depth(self):

        #Ordenamos los valores del eje Z y obtenemos el más alto
        self.df_stacked_front_ele['Z'] = pd.to_numeric(self.df_stacked_front_ele['Z'])
        self.df_stacked_front_ele.sort_values('Z', ascending=False, inplace = True)
        self.max_depth_front = self.df_stacked_front_ele['Z'][0]
        self.df_stacked_back_ele['Z'] = pd.to_numeric(self.df_stacked_back_ele['Z'])
        self.df_stacked_back_ele.sort_values('Z', ascending=False, inplace = True)
        self.max_depth_back = self.df_stacked_back_ele['Z'][0]

    def get_max_curve(self):
        
        #Ordenamos los valores del eje Z y obtenemos el mínimo, que es el que representa la máxima curva (a menor radio, mayor curvatura)
        try:
            self.df_stacked_front_cur['Z'] = self.df_stacked_front_cur['Z'].apply(lambda x: x.replace(',', '.'))
            self.df_stacked_front_cur['Z'] = pd.to_numeric(self.df_stacked_front_cur['Z'])
            self.df_stacked_front_cur.sort_values('Z', ascending=True, inplace = True)
            
            self.df_stacked_back_cur['Z'] = self.df_stacked_back_cur['Z'].apply(lambda x: x.replace(',', '.'))
            self.df_stacked_back_cur['Z'] = pd.to_numeric(self.df_stacked_back_cur['Z'])
            self.df_stacked_back_cur.sort_values('Z', ascending=True, inplace = True)
        except:
            pass
        #como nos devuelve una serie, obtenemos el primer valor de la serie, el cual corresponde con su valor de curvatura máxima
        self.max_curve_front = self.df_stacked_front_cur.min()[0]
        
        self.max_curve_back = self.df_stacked_back_cur.min()[0]

        
    def get_min_curve(self):
        
        #Ordenamos los valores del eje Z y obtenemos el mínimo, que es el que representa la máxima curva (a menor radio, mayor curvatura)
        try:
            self.df_stacked_front_cur['Z'] = self.df_stacked_front_cur['Z'].apply(lambda x: x.replace(',', '.'))
            self.df_stacked_front_cur['Z'] = pd.to_numeric(self.df_stacked_front_cur['Z'])
            self.df_stacked_front_cur.sort_values('Z', ascending=True, inplace = True)
            
            self.df_stacked_back_cur['Z'] = self.df_stacked_back_cur['Z'].apply(lambda x: x.replace(',', '.'))
            self.df_stacked_back_cur['Z'] = pd.to_numeric(self.df_stacked_back_cur['Z'])
            self.df_stacked_back_cur.sort_values('Z', ascending=True, inplace = True)
        except:
            pass
        #como nos devuelve una serie, obtenemos el primer valor de la serie, el cual corresponde con su valor de curvatura máxima
        self.min_curve_front = self.df_stacked_front_cur.max()[0]
        self.min_curve_back = self.df_stacked_back_cur.max()[0]
        
    def get_max_var_curv(self):
        
        try:
            self.get_max_curve()
        except:
            self.max_curve_front = self.df_stacked_front_cur.min()[0]
            self.max_curve_back = self.df_stacked_back_cur.min()[0]
        
        try:
            self.get_min_curve()
        except:
            self.min_curve_front = self.df_stacked_front_cur.max()[0]
            self.min_curve_back = self.df_stacked_back_cur.max()[0]
            
        self.var_curve_front = self.min_curve_front - self.max_curve_front
        self.var_curve_back = self.min_curve_back - self.max_curve_back

    def get_mean_curv(self):
        
        #obtenemos la media de la curvatura de la cornea
        try:
            self.get_max_curve()
        except:
            pass
        self.mean_curve_front = self.df_stacked_front_cur.mean()[0]
        self.mean_curve_back = self.df_stacked_back_cur.mean()[0]
       
    
    def get_pacient_info(self):
        
        #Obtenemos un DataFrame que no esté limitado
        df_stacked = self.df_ele.stack()
        df_stacked = df_stacked.reset_index()
        df_stacked = df_stacked.rename(index = str, columns = {'FRONT': 'X', 'level_1': 'Y', 0: 'Z'})
        #Creamos una nueva columna donde introducimos los valores de los ID para poder hacer transformaciones posteriores
        df_stacked['ID'] = df_stacked.index
        df_stacked['ID'] = pd.to_numeric(df_stacked['ID'])
        #Buscamos en los ID donde se encuentra el campo fecha de nacimiento
        birthdate = df_stacked[df_stacked['X'] == 'DateOfBirth']['Z'].get_values()[0]
        birthdate = datetime.datetime.strptime(birthdate, '%d-%m-%Y')
        #transformamos el dato a fecha y obtenemos la edad del paciente
        self.age = 2019 - int(birthdate.year)
        #para obtener la k_max, realizamos la misma operación que con la edad
        self.k_max = df_stacked[df_stacked['X'] == 'K Max (Front)']['Z'].get_values()[0]
        self.k_max = float(self.k_max.replace(',','.'))
        self.paqui_min = int(df_stacked[df_stacked['X'] == 'Pachy Min']['Z'].get_values()[0])
        #hay casos en los que en los ficheros no viene reflejada la posición (x, y) de la posición del centro de la córnea, por lo que en el caso de no encontramos, situamos la posición en el centro
        try:
            self.x_cornea = df_stacked[df_stacked['X'] == 'Cornea Center Pos X (related to apex, [mm])']['Z'].get_values()[0]
            self.x_cornea = float(self.x_cornea.replace(",", "."))
            self.y_cornea = df_stacked[df_stacked['X'] == 'Cornea Center Pos Y (related to apex, [mm])']['Z'].get_values()[0]
            self.y_cornea = float(self.y_cornea.replace(",", "."))
        except:
            self.x_cornea = 0
            self.y_cornea = 0
        
        #Obtenemos los datos del nombre y el ojo estudiado
        self.first_name = df_stacked[df_stacked['X'] == 'FirstName']['Z'].get_values()[0]
        self.last_name = df_stacked[df_stacked['X'] == 'LastName']['Z'].get_values()[0]
        self.eye = df_stacked[df_stacked['X'] == 'Eye']['Z'].get_values()[0]
        
    def __init__(self, name_ele, name_curv, name_paqui):
        
        #leemos el fichero que nos mandan
        self.df_ele = pd.read_csv(name_ele, sep = ';', index_col= 0, header = 0, encoding = "ISO-8859-1")
        self.df_curv = pd.read_csv(name_curv, sep = ';', index_col= 0, header = 0, encoding = "ISO-8859-1")
        self.df_paqui = pd.read_csv(name_paqui, sep = ';', index_col= 0, header = 0, encoding = "ISO-8859-1")
        #enviamos las transformaciones necesarias para poder obtener los valores necesarios para entrenar nuestro clasificador
        self.stack_and_transform_front(self.df_ele, 1)
        self.stack_and_transform_front(self.df_curv, 2)
        self.stack_and_get_axis(self.df_paqui)
        self.get_max_depth()
        self.get_max_curve()
        self.get_max_var_curv()
        self.get_mean_curv()
        self.get_pacient_info()
        self.get_max_distance()
        #sacamos los valores necesarios en un vector para poder trabajar con el posteriormente
        self.x = [self.max_depth_front, self.max_depth_back, self.max_curve_front, self.max_curve_back, self.var_curve_front, self.var_curve_back, self.mean_curve_front, self.mean_curve_back, self.age, self.k_max, self.paqui_min, self.distance, self.max_curve_pos_rel_to_center]
        self.pacient_info = [self.first_name, self.last_name, self.eye]
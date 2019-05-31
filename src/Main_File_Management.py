# -*- coding: utf-8 -*-
"""
Created on Sun May 26 18:39:58 2019

@author: Diego Álvarez Fernández
"""

from os import listdir
from os.path import isfile, join
import shutil

if __name__ == "__main__":
    #introducimos la ruta donde vamos a contener todos los archivos sacados de la máquina especializada en topografía ocular
    mypath = 'C:/Users/lique/Desktop/Mapas para estudio'
    #listamos los ficheros que contiene dicha carpeta
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    lista_ficheros = []
    #de dicha lista sacamos aquellos que nos interesan (hay muchos que no son necesarios)
    for i in range(len(onlyfiles)):
        if onlyfiles[i][-8:] == "_ELE.CSV" or onlyfiles[i][-8:] == "_CUR.CSV" or onlyfiles[i][-8:] == "_PAC.CSV":
            lista_ficheros.append(onlyfiles[i])
    dest_path = "C:/Users/lique/OneDrive/Documents/GitHub/master-data-science/"
    orig_path = "C:/Users/lique/Desktop/Mapas para estudio/"
    #dichos ficheros los movemos a otra carpeta para poder gestionarlos posteriormente
    for i in range(len(lista_ficheros)):
        shutil.move(orig_path + lista_ficheros[i], dest_path + lista_ficheros[i])  
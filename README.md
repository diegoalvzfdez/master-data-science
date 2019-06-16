# Trabajo Fin de Máster

## Sistema de clasificación de pacientes con queratocono como apoyo a la toma de decisiones de un especialista.

### Realizado por: Diego Álvarez Fernández

------------------------------------------------------------------------------------------------------------------

# Introducción

Hoy en día, en el mundo de la medicina, las innovaciones en términos de avances tecnológicos están a la orden del día. Cientos de ingenieros, investigadores y especialistas centran sus esfuerzos en mejorar tanto las infraestructuras de los centros clínicos como la vida de las personas que se encuentran hospitalizadas, ya sea mejorando las terapias de rehabilitación o la calidad de vida de los mismos.

En el presente proyecto vamos a intentar crear un sistema de apoyo a la toma de decisiones de un cirujano especializado en la patología del queratocono. Para establecer un punto de partida, vamos a dar unas pequeñas referencias acerca de dicha patología. El queratocono podemos definirlo como una patalogía degenerativa que afecta a la cornea del ojo. Debido a la alteración del colágeno de la córnea, el ojo toma un aspecto irregular, lo cual es un elemento característico de dicha patología. El proceso degenerativo de la córnea provoca que éste acabe tomando un aspecto de un cono, lo cual da nombre a la enfermedad a la cual nos referimos. 

Cuando un paciente presenta los síntomas de un queratocono, el especialista puede tomar tres tipos de decisiones: no operar al paciente, ya que la patología no está lo suficientemente avanzada, operar al paciente mediante anillos (o segmentos corneales intraestromales) u operar al paciente mediante crosslinking. Mediante la creación de nuestro sistema de clasificación, vamos a tratar de crear un software que nos de un feedback analizando los mapas de elevación, curvatura y paquimetría del paciente. 

--------------------------------------------------------------------------------------------------------------------

# Punto inicial

Los datos son los obtenidos a partir del Oculus Pentacam. Esta tecnología contiene una máquina rotatoria que captura imágenes del segmento anterior del ojo. Mediante estas imágenes, el software de dicha tecnología nos permite obtener los mapas de elevación, de curvatura y paquimétricos del ojo del paciente. La máquina tiene el siguiente aspecto:

![Pentacam](https://raw.githubusercontent.com/diegoalvzfdez/master-data-science/master/imgs/OCULUS_Pentacam(1).jpg)

Como ya nos podemos imaginar, esta tecnología no es utilizada únicamente para el estudio y diagnóstico de pacientes con la enfermedad del queratonoco. En la base de datos de esta máquina se encuentran multitud de pacientes con diferentes patologías, por lo que la labor de extracción de los datos es tediosa y complicada. Se han obtenido muestras de 461 ojos con queratocono, los cuales se han etiquetado entre: No operados, operados mediante Crosslinking y operados mediante anillos. Estas etiquetas son las que posteriormente nos permitirán configurar nuestros clasificadores.

Una vez hemos obtenido los ficheros del Oculus Pentacam, obtenemos un conjunto de ficheros por usuario, de los cuales tenemos que aislar los 3 ficheros csv que nos interesan. En este punto es donde entra nuestro primer Script: Main_File_Management.py. Este Script nos permite pasar de una carpeta a otra de nuestro equipo aquellos ficheros que son útiles para nuestro proyecto. Afortunadamente, podemos distinguir los ficheros que necesitamos del resto, ya que finalizan por "_cur.csv", "_ele.csv" y "_pac.csv". Gracias a esto, podemos tener en 3 carpetas diferentes las muestras sin operar y las muestras operadas mediante crosslinking y mediante anillos.

![Ficheros](https://raw.githubusercontent.com/diegoalvzfdez/master-data-science/master/imgs/Ficheros.png)


--------------------------------------------------------------------------------------------------------------------

# Tratamiento de los ficheros del Pentacam

Una vez hemos finalizado con la extracción y la gestión de los datos obtenidos del Oculus Pentacam, nuestro siguiente paso es obtener un Dataset con la información necesaria para poder entrenar un clasificador. En una primera instancia, lo que hemos obtenido en la extracción tiene un aspecto similar a esto (se puede encontrar en este repositorio un ejemplo anonimizado de los csv obtenidos en la extracción del Pentacam):

![csv](https://raw.githubusercontent.com/diegoalvzfdez/master-data-science/master/imgs/csv%20obtenido%20de%20la%20extracción.PNG)

Como se puede observar, lo que obtenemos es un conjunto de mapas, en los cuales se pinta un eje X, un eje Y, y los valores de elevación/curvatura/paquimetría correspondientes a dichas coordenadas. De todos los mapas presentes en el csv, sólamente nos interesan los dos primeros, que corresponden a la cara posterior y a la cara anterior del ojo. Además, una vez pasamos todos los mapas, en el csv se encuentran una serie de datos que también son relevantes a la hora de entrenar nuestro clasificador. En este punto, entra a escena nuestro segundo Script creado: Main.py. Este Script es el encargado de generar los ficheros ya procesados con los que podemos entrenar nuestro clasificador. 

A la hora de elegir cómo programar nuestro Script, se eligió emplear Python ya que se requería el uso de la librería Pandas y se decidió no generar el código mediante un Notebook. Esto es debido a que se pretende en un futuro poder realizar esta funcionalidad mediante una interfaz gráfica, en la cual el usuario únicamente debe seleccionar dónde se encuentran los ficheros generados por Pentacam para obtenerlos posteriormente ya tratados (y posteriormente introducirlos directamente a un clasificador para obtener la predicción del paciente). Se ha generado también una libreria, en la cual hemos creado los métodos necesarios para obtener los datos requeridos por el predictor. Esta libreria se puede encontrar en la carpeta /src, llamada managecsv.py.

El funcionamiento del Script es muy sencillo. Una vez ejecutado, el Script pide al usuario la ruta donde se encuentran los ficheros a tratar. Mediante Pop Ups, pregunta en primer lugar qué tipo de datos son los que le van a llegar (si son pacientes operados o no), para despues abrir una ventana emergente donde el usuario debe seleccionar en qué carpeta se encuentran los ficheros csv. El preguntar al usuario que tipo de pacientes son los que va a introducir es lo que nos permite etiquetar las muestras que nos van llegando. Una vez el usuario selecciona dónde se encuentran los ficheros, el Script obtiene la siguiente información de los mapas (elevación, curvatura y paquimétrico) del paciente:

- Máxima Elevación de la cara Frontal.
- Máxima Elevación de la cara Anterior.
- Máxima Curvatura de la cara Frontal.
- Máxima Curvatura de la cara Anterior.
- Máxima Diferencia de Curvatura de la cara Frontal.
- Máxima Diferencia de Curvatura de la cara Anterior.
- Media de las Curvaturas de la cara Frontal.
- Media de las Curvaturas de la cara Anterior.
- Edad del Paciente.
- K Máxima.
- Paquimetría mínima.
- Distancia entre el punto de Máxima Curvatura y Mínima Paquimetría.
- Distancia del punto de Máxima Curvatura con respecto al centro de la córnea.
- Tratamiento.

Tratando todos los ficheros de los pacientes los cuales no se han operado, y los operados mediante las técnicas de crosslinking y anillos, obtenemos el fichero ya procesado que podemos observar en la carpeta /preprocessed_data del presente repositorio.


--------------------------------------------------------------------------------------------------------------------

# Dataset Preprocesado

Una vez ya hemos obtenido el Dataset con el cual podemos trabajar, podemos pasar a la fase de estudiar los datos que hemos obtenido. En esta fase, pasamos a realizar la programación en R, creando un Script que nos permitirá obtener las gráficas necesarias para poder entender los datos a los cuales nos enfrentamos. 

En una primera instancia, lo primero que debemos hacer es estudiar los histogramas de nuestro Dataset para poder observar cómo se agrupan todas las variables de nuestro sistema. Además, ggplot nos permite visualizar los diferentes histogramas desglosados por una variable, que en este caso es el tratamiento que se ha dado al paciente. 

En el siguiente link se puede observar los gráficos creados mediante ggplot para estudiar los datos preprocesados:

[Visualización de los datos preprocesados](https://diegoalvzfdez.github.io/) 

Con estos gráficos lo que se pretende es encontrar cierta relación entre las variables que hemos generado en nuestros Scripts y sus distribuciones. Así, podemos buscar si se ha generado algun tipo de dato corrupto, que altere las distribuciones y que sea perjudicial a la hora de realizar una predicción. Con estos gráficos hemos podido sacar una cierta serie de conclusiones que nos ayudan a entender un poco más los datos a los cuales nos enfrentamos:

- Las elevaciones producidas en la córnea no nos permiten diferenciar que tipo de tratamiento se ha recomendado al paciente.
- Los pacientes a los cuales no se les ha practicado ningun tipo de cirugía tienen una curvatura mucho menos acentuada que los pacientes a los cuales si se les ha practicado una cirugía. 
- Además, los pacientes operados tenían una mayor desviación de curvaturas en su córnea con respecto a los pacientes sin operar.
- Se opera antes a los pacientes más jóvenes que a los ancianos. 
- Se observa una mayor K máxima en aquellos pacientes a los cuales se les ha realizado alguna operación.
- Por otro lado, los pacientes operados tienen una menor paquimetría mínima con respecto a los operados.
- Podemos observar que a mayor curvatura máxima (la curvatura se mide por el radio, a menor radio, mayor curvatura), se encuentra una menor paquimetría mínima.


--------------------------------------------------------------------------------------------------------------------

# Modelado

En este último punto, se ha tratado de entrenar un sistema de clasificación para poder dar una predicción sobre el tratamiento al que hay que someter a un paciente. Se describirán los tratamientos que se han dado a los datos al igual que los modelos que se han empleado, mostrando las métricas y conclusiones obtenidas. En este caso, para la creación de los modelos se ha empleado el lenguaje Python, programado en un notebook. En este caso se ha obtado por un Notebook ya que nos permite iterar constantemente para obtener los resultados más óptimos.

## 1º Paso: Estudio de las correlaciones entre los parámetros

Antes de crear ningún modelo, el primer paso a dar es estudiar las distintas correlaciones entre los diferentes parámetros. Mediante este estudio, lo que se pretende es eliminar al máximo las correlaciones, ya que estas dificultan las labores predictivas de los modelos. La primera tabla de correlaciones tiene un aspecto parecido al siguiente:

![Correlaciones](https://raw.githubusercontent.com/diegoalvzfdez/master-data-science/master/imgs/Correlaciones.png)

Como se puede observar, hay una gran correlación entre los parámetros que son compartidos entre la parte posterior y la parte anterior de la córnea. Por ejemplo, existe una gran correlación entre la máxima elevación de la cara posterior con la cara anterior. Por tanto, se decide obtener, entre las dos caras, los valores más extremos, ya que son lo que determinan si un paciente se debe operar o no. Entonces, de las elevaciones se cogerá el valor más alto y de las curvaturas el valor mínimo (ya que a menor radio, mayor curvatura).

Tras realizar estos cambios, se observar que el número de muestras entre pacientes operados, operados mediante crosslinking y operados mediante anillos está muy desbalanceado. Esto hace que la predicción pase a ser si un paciente debe ser operado o no, ya que esta agrupación hace que los dos conjuntos de muestras estén mucho más balanceados (230 paciente no operados frente a 231 pacientes operados)

## 2º Paso: Búsqueda del modelo

En este punto vamos a ir probando modelos en búsqueda de aquel que nos de mejores métricas a la hora de predecir si a un usuario se le debe operar o no. Para ello, enumeraremos los modelos empleados, los hiperparámetros escogidos y las métricas obtenidas. Las métricas se mostrarán las obtenidas mediante el método train_test_split y el método cross_validation_score.

### Regresión Logística.

- Mediante Cross Validation: se obtuvo una media del Accuracy del 73 %

- Mediante Train Test Split: se obtuvo una matriz de confusión de este tipo:

![Regresión Logística](https://raw.githubusercontent.com/diegoalvzfdez/master-data-science/master/imgs/Reg_Log.png)

Con un Accuracy del 75.56 %, una precisión para los pacientes operados de un 77% y una precisión para los pacientes no operados del 75 %.

### K Nearest Neighbors

- Hiperparámetros elegidos:

  n_neighbors = 9

- Mediante Cross Validation: Obtenido un Accuracy medio de un 61.38 %.

- Mediante Train Test Split: se obtuvo una matriz de confusión de este tipo:

![KN](https://raw.githubusercontent.com/diegoalvzfdez/master-data-science/master/imgs/KN.png)

Con un Accuracy del 65,46%, una precisión para los pacientes operados de un 68% y una precisión para los pacientes no operados de un 63 %

### SVM (Kernel Linear)

- Hiperparámetros elegidos:

  C = 1000
  
 - Mediante Cross Validation: Obtenido un Accuracy medio del 73.96%
 
 - Mediante Train Test Split: se obtuvo una matriz de confusión de este tipo:
 
 ![SVM](https://raw.githubusercontent.com/diegoalvzfdez/master-data-science/master/imgs/SVM.png)
 
 Con un Accuracy del 71,22%, una precisión para los pacientes operados de un 75% y una precisión para los pacientes no operados de un 68 %

### Decision Trees

- Hiperparámetros elegidos:

  min_samples_leaf = 7
  
  max_depth = 13

- Mediante Cross Validation: Obtenido un Accuracy medio del 70.28 %

- Mediante Train Test Split: se obtuvo una matriz de confusión de este tipo:

![Decision Tree](https://raw.githubusercontent.com/diegoalvzfdez/master-data-science/master/imgs/Decision_Tree.png)

Con un Accuracy del 64,02%, una precisión para los pacientes operados de un 66% y una precisión para los pacientes no operados de un 62 %

### Random Forest

- Hiperparámetros elegidos:


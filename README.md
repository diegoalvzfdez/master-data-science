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

Los datos son los obtenidos a partir del Oculus Pentacam. Esta máquina contiene una máquina rotatoria que captura imágenes del segmento anterior del ojo. Mediante estas imágenes, el software de dicha tecnología nos permite obtener los mapas de elevación, de curvatura y paquimétricos del ojo del paciente. La máquina tiene el siguiente aspecto:

![Pentacam](https://raw.githubusercontent.com/diegoalvzfdez/master-data-science/master/imgs/OCULUS_Pentacam(1).jpg)

Como ya nos podemos imaginar, esta tecnología no es utilizada únicamente para el estudio y diagnóstico de pacientes con la enfermedad del queratonoco. En la base de datos de esta máquina se encuentran multitud de pacientes con diferentes patologías, por lo que la labor de extracción de los datos es tediosa y complicada. Se han obtenido muestras de 461 ojos con queratocono, los cuales se han etiquetado entre: No operados, operados mediante Crosslinking y operados mediante anillos. Estas etiquetas son las que posteriormente nos permitirán configurar nuestros clasificadores.

Una vez hemos obtenido los ficheros del Oculus Pentacam, obtenemos un conjunto de ficheros por usuario, de los cuales tenemos que aislar los 3 ficheros csv que nos interesan. En este punto es donde entra nuestro primer Script: Main_File_Management.py. Este Script nos permite pasar de una carpeta a otra de nuestro equipo aquellos ficheros que son útiles para nuestro proyecto. Afortunadamente, podemos distinguir los ficheros que necesitamos del resto, ya que finalizan por "_cur.csv", "_ele.csv" y "_pac.csv". Gracias a esto, podemos tener en 3 carpetas diferentes las muestras sin operar y las muestras operadas mediante crosslinking y mediante anillos.

![Ficheros](https://raw.githubusercontent.com/diegoalvzfdez/master-data-science/master/imgs/Ficheros.png)


--------------------------------------------------------------------------------------------------------------------

# Tratamiento de los ficheros del Pentacam

Una vez hemos finalizado con la extracción y la gestión de los datos obtenidos del Oculus Pentacam, nuestro siguiente paso es obtener un Dataset con la información necesaria para poder entrenar un clasificador. En una primera instancia, lo que hemos obtenido en la extracción tiene un aspecto similar a esto (se puede encontrar en este repositorio un ejemplo anonimizado de los csv obtenidos en la extracción del Pentacam):

![csv](https://raw.githubusercontent.com/diegoalvzfdez/master-data-science/master/imgs/csv%20obtenido%20de%20la%20extracción.PNG)

Como se puede observar, lo que obtenemos es un conjunto de mapas, en los cuales se pinta un eje X, un eje Y, y los valores de elevación/curvatura/paquimetría correspondientes a dichas coordenadas. De todos los mapas presentes en el csv, sólamente nos interesan los dos primeros, que corresponden a la cara posterior y a la cara anterior del ojo. Además, una vez pasamos todos los mapas, en el csv se encuentran una serie de datos que también son relevantes a la hora de entrenar nuestro clasificador. En este punto, entra a escena nuestro segundo Script creado: Main.py. Este Script es el encargado de generar los ficheros ya procesados que con los que podemos entrenar nuestro clasificador. 

A la hora de elegir cómo programar nuestro Script, se eligió emplear Python ya que se requería el uso de la librería Pandas y se decidió no generar el código mediante un Notebook. Esto es debido a que se pretende en un futuro poder realizar esta funcionalidad mediante una interfaz gráfica, en la cual el usuario únicamente debe seleccionar dónde se encuentran los ficheros generados por Pentacam para obtenerlos posteriormente ya tratados (y posteriormente introducirlos directamente a un clasificador para obtener la predicción del paciente). Se ha generado también una libreria, en la cual hemos creado los métodos necesarios para obtener los datos requeridos por el predictor. Esta libreria se puede encontrar en la carpeta /src, llamada managecsv.py.

El funcionamiento del Script es muy sencillo. Una vez ejecutado, el Script pide al usuario la ruta donde se encuentran los ficheros a tratar. Mediante Pop Ups, pregunta en primer lugar que tipo de datos son los que le van a llegar (si son pacientes operados o no), para despues abrir una ventana emergente donde el usuario debe seleccionar en qué carpeta se encuentran los ficheros csv. El preguntar al usuario que tipo de pacientes son los que va a introducir es lo que nos permite etiquetar las muestras que nos van llegando. Una vez el usuario selecciona donde se encuentran los ficheros, el Script obtiene la siguiente información de los mapas (elevación, curvatura y paquimétrico) del paciente:

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








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

Los datos son los obtenidos a partir del Oculus Pentacam. Esta máquina contiene una máquina rotatoria que captura imágenes del segmento anterior del ojo. Mediante estas imágenes, el software de dicha tecnología nos permite obtener los mapas de elevación, de curvatura y paquimétricos. La máquina tiene el siguiente aspecto:

![Pentacam](https://raw.githubusercontent.com/diegoalvzfdez/master-data-science/master/imgs/OCULUS_Pentacam(1).jpg)

Como ya nos podemos imaginar, esta tecnología no es utilizada únicamente para el estudio y diagnóstico de pacientes con la enfermedad del queratonoco. En la base de datos de esta máquina se encuentran multitud de pacientes con diferentes patologías, por lo que la labor de extracción de los datos es tediosa y complicada. Se han obtenido muestras de 461 ojos con queratocono, los cuales se han etiquetado entre: No operados, operados mediante Crosslinking y operados mediante anillos. Estas etiquetas son las que posteriormente nos permitirán configurar nuestros clasificadores.

Una vez hemos obtenido los ficheros del Oculus Pentacam, obtenemos un conjunto de ficheros por usuario, de los cuales tenemos que aislar los 3 ficheros csv que nos interesan. En este punto es donde entra nuestro primer Script: Main_File_Management.py. Este Script nos permite pasar de una carpeta a otra de nuestro equipo aquellos ficheros que son útiles para nuestro proyecto. Afortunadamente, podemos distinguir los ficheros que necesitamos del resto, ya que finalizan por "_cur.csv", "_ele.csv" y "_pac.csv". Gracias a esto, podemos tener en 3 carpetas diferentes las muestras sin operar y las muestras operadas mediante crosslinking y mediante anillos.

![Ficheros](https://raw.githubusercontent.com/diegoalvzfdez/master-data-science/master/imgs/Ficheros.jpg)

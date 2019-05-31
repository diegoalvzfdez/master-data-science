##########################################################################
# Diego Álvarez Fernandez 
# Master Data Science: TFM
########################################################################

library(dplyr)
library(ggplot2)
library(sqldf)

#vamos a realizar gráficos para tener una visión de los datos con los que estamos tratando

eye_data <- data.table::fread('C:/Users/lique/OneDrive/Documents/GitHub/master-data-science/preprocessed_data/csv_eye.csv', sep = ";")

max.depth.by.year <- sqldf("select Age, Avg(`Max Depth Front`) as AVGMaxDepthFront, AVG(`Max Depth Back`) as AVGMaxDepthBack from eye_data group by Age order by Age asc")

#podemos observar la distribución de las máximas elevaciones, tanto de la parte anterior como de la parte posterior, en función de la edad
max.depth.front.by.age <- ggplot(max.depth.by.year, aes(x = Age, y = AVGMaxDepthFront)) + geom_point() + geom_point(aes(color=Age))
max.depth.back.by.age <- ggplot(max.depth.by.year, aes(x = Age, y = AVGMaxDepthBack)) + geom_point() + geom_point(aes(color=Age))
max.depth.back.by.age
max.depth.front.by.age

#una buena manera de observar lo que tenemos en nuestro DataSet es dibujando los histogramas que obtenemos

#podemos observar el histograma de la máxima profundidad posterior
max.depth.front <- sqldf("select `Max Depth Front` as MaxDepthFront from eye_data")
max.depth.front.hist <- ggplot(max.depth.front, aes(x = MaxDepthFront)) + geom_histogram(binwidth = 50)
max.depth.front.hist

#podemos observar el histograma de la máxima profundidad anterior
max.depth.back <- sqldf("select `Max Depth Back` as MaxDepthBack from eye_data")
max.depth.back.hist <- ggplot(max.depth.back, aes(x = MaxDepthBack)) + geom_histogram(binwidth = 50)
max.depth.back.hist

#podemos estudiar la relación entre la curvatura máxima y la elevación máxima

max.depth.curve.front <- sqldf("select `Max Depth Front` as MaxDepthFront, `Max Curve Front` as MaxCurveFront from eye_data")
#limitamos los valores de máxima curvatura para evitar errores
max.depth.curve.front <- filter(max.depth.curve.front, MaxCurveFront > 0)
depth.vs.curve.front <- ggplot(max.depth.curve.front, aes(x = MaxDepthFront, y = MaxCurveFront)) + geom_point() + theme_minimal()
depth.vs.curve.front

#podemos ver la edad media de los pacientes por tratamiento

avg.age.per.treatment <- sqldf("select Avg(`Age`) as AvgAge, `Treatment` from eye_data group by Treatment ")
age.vs.treatment <- ggplot(avg.age.per.treatment, aes(x = Treatment, y = AvgAge)) + geom_col() + theme_minimal()
age.vs.treatment



##########################################################################
# Diego Álvarez Fernandez 
# Master Data Science: TFM
########################################################################

list.of.packages <- c("R.utils", "tidyverse", "doParallel", "foreach", "sqldf")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) install.packages(new.packages)

library(dplyr)
library(ggplot2)
library(sqldf)

#vamos a realizar gráficos para tener una visión de los datos con los que estamos tratando

eye_data <- data.table::fread('C:/Users/lique/OneDrive/Documents/GitHub/master-data-science/preprocessed_data/csv_eye.csv', sep = ";")

max.depth.by.year <- sqldf("select Age, Avg(`Max Depth Front`) as AVGMaxDepthFront, AVG(`Max Depth Back`) as AVGMaxDepthBack from eye_data group by Age order by Age asc")

#podemos observar la distribución de las máximas elevaciones, tanto de la parte anterior como de la parte posterior, en función de la edad
max.depth.front.by.age <- ggplot(max.depth.by.year, aes(x = Age, y = AVGMaxDepthFront)) + geom_point() + geom_point(aes(color=Age))
max.depth.back.by.age <- ggplot(max.depth.by.year, aes(x = Age, y = AVGMaxDepthBack)) + geom_point() + geom_point(aes(color=Age))

#una buena manera de observar lo que tenemos en nuestro DataSet es dibujando los histogramas que obtenemos

max.depth.front <- sqldf("select `Max Depth Front` as MaxDepthFront from eye_data")
max.depth.front.hist <- ggplot(max.depth.front, aes(x = MaxDepthFront)) + geom_histogram(binwidth = 50)
max.depth.front.hist

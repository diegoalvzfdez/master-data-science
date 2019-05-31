##########################################################################
# Diego Álvarez Fernandez 
# Master Data Science: TFM
########################################################################

library(dplyr)
library(ggplot2)
library(sqldf)
library(ggthemes)


#vamos a realizar gráficos para tener una visión de los datos con los que estamos tratando

eye_data <- data.table::fread('C:/Users/lique/OneDrive/Documents/GitHub/master-data-science/preprocessed_data/csv_eye.csv', sep = ";")

#debido a que los nombres de los campos del csv vienen con espacios, y no se me ocurre mejor manera para tratarlos, emplearemos SQL para sacar las tablas necesarias para nuestro modulo de explotación
max.depth.by.year <- sqldf("select Age, Avg(`Max Depth Front`) as AVGMaxDepthFront, AVG(`Max Depth Back`) as AVGMaxDepthBack from eye_data group by Age order by Age asc")

#podemos observar la distribución de las máximas elevaciones, tanto de la parte anterior como de la parte posterior, en función de la edad
max.depth.front.by.age <- ggplot(max.depth.by.year, aes(x = Age, y = AVGMaxDepthFront)) + 
                            geom_point() + 
                            geom_point(aes(color=Age)) + 
                            labs(title="Promedio de las máximas elevaciones de la\nparte posterior del ojo frente a la edad del \npaciente", 
                                 caption = "Diego Álvarez Fernández")+ 
                            theme_minimal()

max.depth.back.by.age <- ggplot(max.depth.by.year, aes(x = Age, y = AVGMaxDepthBack)) + 
                            geom_point() + 
                            geom_point(aes(color=Age)) +
                            labs(title="Promedio de las máximas elevaciones de la\nparte anterior del ojo frente a la edad del \npaciente", 
                                 caption = "Diego Álvarez Fernández") + 
                            theme_minimal()
max.depth.back.by.age
max.depth.front.by.age

#una buena manera de observar lo que tenemos en nuestro DataSet es dibujando los histogramas que obtenemos

#podemos observar el histograma de la máxima profundidad posterior
max.depth.front <- sqldf("select `Max Depth Front` as MaxDepthFront, `Treatment` from eye_data")
max.depth.front.hist <- ggplot(max.depth.front, aes(x = MaxDepthFront)) + 
                            geom_histogram(binwidth = 50) +
                            labs(title="Histograma de las máximas elevaciones de la zona \nposterior del ojo del paciente", 
                                 caption = "Diego Álvarez Fernández") + 
                            theme_tufte()
max.depth.front.hist

#además, podemos crear un histograma en función del tratamiento dado al paciente

max.depth.front.hist.by.treatment <- ggplot(max.depth.front, aes(x = MaxDepthFront, fill = Treatment)) + 
                                        geom_histogram(binwidth = 50)+
                                        labs(title="Histograma de las máximas elevaciones de la \nzona posterior del ojo del paciente en \nfunción del tratamiento dado", 
                                             caption = "Diego Álvarez Fernández") + 
                                        theme_tufte()
max.depth.front.hist.by.treatment

#podemos observar el histograma de la máxima profundidad anterior
max.depth.back <- sqldf("select `Max Depth Back` as MaxDepthBack, `Treatment` from eye_data")
max.depth.back.hist <- ggplot(max.depth.back, aes(x = MaxDepthBack)) + 
                          geom_histogram(binwidth = 50) +
                          labs(title="Histograma de las máximas elevaciones de la \nzona anterior del ojo del paciente en función \ndel tratamiento dado", 
                               caption = "Diego Álvarez Fernández") + 
                          theme_tufte()
                          
max.depth.back.hist

#podemos hacer lo mismo, identificando los resultados por tratamiento

max.depth.back.hist.by.treatment <- ggplot(max.depth.back, aes(x = MaxDepthBack, fill = Treatment)) + geom_histogram(binwidth = 50)
max.depth.back.hist.by.treatment

#podemos estudiar la relación entre la curvatura máxima y la elevación máxima
max.depth.curve.front <- sqldf("select `Max Depth Front` as MaxDepthFront, `Max Curve Front` as MaxCurveFront, `Treatment` from eye_data")
#limitamos los valores de máxima curvatura para evitar errores
max.depth.curve.front <- filter(max.depth.curve.front, MaxCurveFront > 0)
depth.vs.curve.front <- ggplot(max.depth.curve.front, aes(x = MaxDepthFront, y = MaxCurveFront)) + 
                          geom_jitter() +
                          labs(title="Gráfico de dispersión entre la máxima profundidad \ny la máxima curvatura de la zona posterior del ojo", 
                               caption = "Diego Álvarez Fernández") + 
                          theme_tufte()
depth.vs.curve.front

#podemos ver la evolución de esta relación comparándola con el tratamiento dado

depth.vs.curve.front.with.treatment <-  ggplot(max.depth.curve.front, aes(x = MaxDepthFront, y = MaxCurveFront, colour = Treatment)) + 
                                          geom_point() +
                                          labs(title="Gráfico de dispersión entre la máxima profundidad \ny la máxima curvatura de la zona posterior del ojo \nen función del tratamiento", 
                                               caption = "Diego Álvarez Fernández") + 
                                          theme_tufte()
depth.vs.curve.front.with.treatment

#podemos ver la edad media de los pacientes por tratamiento

avg.age.per.treatment <- sqldf("select Avg(`Age`) as AvgAge, `Treatment` from eye_data group by Treatment ")
age.vs.treatment <- ggplot(avg.age.per.treatment, aes(x = Treatment, y = AvgAge)) + 
                      geom_col() + 
                      labs(title="Media de edades de los pacientes por el tratamiento indicado", 
                           caption = "Diego Álvarez Fernández") +
                      theme_tufte()
age.vs.treatment

#dos parámetros interesantes de estudio son la máxima curvatura y la paquimetría mínima, por lo que podemos comparar la evolución de ambas

paqui.and.curve <- sqldf("select `Max Curve Front` as MaxCurveFront, `Paqui Min` as PaquiMin, `Treatment` from eye_data")
#filtramos los valores de máxima curvatura para evitar los que están corruptos
paqui.and.curve <- filter(paqui.and.curve, MaxCurveFront > 0)
#aplicamos una regresión lineal para observar la evolución de la paquimetría con la máxima curvatura
paqui.vs.curve <- ggplot(paqui.and.curve, aes(x = MaxCurveFront, y = PaquiMin)) + 
                    geom_jitter(aes(color = MaxCurveFront)) + 
                    theme_tufte() + 
                    geom_smooth(lwd=1, se=FALSE, method="lm", col="black") + 
                    labs(title="Gráfico de dispersión de la máxima curvatura posterior \nfrente a la mínima paquimetría", 
                          caption = "Diego Álvarez Fernández")
paqui.vs.curve

#como estas dos características son importantes para la elección del tratamiento, podemos comprobar la evolución con respecto al tratamiento
paqui.vs.curve.with.treatment <- ggplot(paqui.and.curve, aes(x = MaxCurveFront, y = PaquiMin, colour = Treatment)) + 
                                    geom_jitter() + 
                                    theme_tufte() + 
                                    geom_smooth(lwd=1, se=FALSE, method="lm", col="black") + 
                                    labs(title="Gráfico de dispersión de la máxima curvatura posterior \nfrente a la mínima paquimetría en función del \ntratamiento", 
                                         caption = "Diego Álvarez Fernández")

paqui.vs.curve.with.treatment

#podemos ver el número de casos que tenemos por tratamiento, en función de la edad
age.per.treatment <- sqldf("select `Age`, `Treatment` from eye_data")
age.vs.treatment.density <- ggplot(age.per.treatment, aes(x = Age, fill = Treatment)) + 
                              geom_density(alpha = 0.2) + 
                              theme_tufte() + 
                              labs(title="Gráfico de densidad de la distribución de edades en \nfunción del tratamiento", 
                                   caption = "Diego Álvarez Fernández")
age.vs.treatment.density

#Otra opción para ver la distribución de una variable es comparándola contra todos los tratamientos, en este caso podemos comparar el histograma de la k máxima
k_max.and.treatment <- sqldf("select `K Max` as KMax, `Treatment` from eye_data")
k_max.and.treatment <- filter(k_max.and.treatment, KMax < 200)
k_max.vs.treatment <- ggplot(k_max.and.treatment, aes(x = KMax, colour = )) + 
                        geom_histogram(binwidth = 2) + 
                        facet_wrap(~ Treatment) + 
                        theme_tufte() + 
                        labs(title="Histogramas de las K máximas en función del \ntratamiento", 
                             caption = "Diego Álvarez Fernández")
k_max.vs.treatment


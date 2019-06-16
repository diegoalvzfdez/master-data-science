##########################################################################
# Diego Álvarez Fernandez 
# Master Data Science: TFM
########################################################################

library(dplyr)
library(ggplot2)
library(sqldf)
library(ggthemes)
library(ggpubr)


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

max.depth.front.by.age

max.depth.back.by.age <- ggplot(max.depth.by.year, aes(x = Age, y = AVGMaxDepthBack)) + 
                            geom_point() + 
                            geom_point(aes(color=Age)) +
                            labs(title="Promedio de las máximas elevaciones de la\nparte anterior del ojo frente a la edad del \npaciente", 
                                 caption = "Diego Álvarez Fernández") + 
                            theme_minimal()
max.depth.back.by.age


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
                          labs(title="Histograma de las máximas elevaciones de la \nzona anterior del ojo del paciente", 
                               caption = "Diego Álvarez Fernández") + 
                          theme_tufte()
                          
max.depth.back.hist

#podemos hacer lo mismo, identificando los resultados por tratamiento

max.depth.back.hist.by.treatment <- ggplot(max.depth.back, aes(x = MaxDepthBack, fill = Treatment))+ 
                                        geom_histogram(binwidth = 50) +
                                        labs(title="Histograma de las máximas elevaciones de la \nzona anterior del ojo del paciente en función \ndel tratamiento dado", 
                                             caption = "Diego Álvarez Fernández") + 
                                        theme_tufte()
max.depth.back.hist.by.treatment

#por otro lado, podemos visualizar los histogramas de las curvaturas, con la información sesgada por tratamiento dado

max.curve.front <- sqldf("select `Max Curve Front` as MaxCurveFront, `Treatment` from eye_data")
max.curve.front <- filter(max.curve.front, MaxCurveFront > 0)
max.curve.front.hist <- ggplot(max.curve.front, aes(x = MaxCurveFront, fill = Treatment)) + 
                          geom_histogram(binwidth = 0.1)+
                          labs(title="Histograma de las máximas curvaturas de la \nzona posterior del ojo del paciente en función \ndel tratamiento dado", 
                               caption = "Diego Álvarez Fernández") + 
                          theme_tufte()
max.curve.front.hist

max.curve.back <- sqldf("select `Max Curve Back` as MaxCurveBack, `Treatment` from eye_data")
max.curve.back <- filter(max.curve.back, MaxCurveBack > 0)
max.curve.back.hist <- ggplot(max.curve.back, aes(x = MaxCurveBack, fill = Treatment)) + 
                          geom_histogram(binwidth = 0.1)+
                          labs(title="Histograma de las máximas curvaturas de la \nzona anterior del ojo del paciente en función \ndel tratamiento dado", 
                               caption = "Diego Álvarez Fernández") + 
                          theme_tufte()
max.curve.back.hist

#podemos estudiar tambien los histogramas de las máximas desviaciones de las curvaturas en función del tratamiento dado

max.var.curve.front <- sqldf("select `Max Variation Curve Front` as MaxVariationCurveFront, `Treatment` from eye_data")
max.var.curve.front <- filter(max.var.curve.front, MaxVariationCurveFront > 0)
max.var.curve.front.hist <- ggplot(max.var.curve.front, aes(x = MaxVariationCurveFront, fill = Treatment)) + 
                              geom_histogram(binwidth = 0.1) +
                              labs(title="Histograma de las máximas desviaciones de las curvaturas de la \nzona posterior del ojo del paciente en función \ndel tratamiento dado", 
                                   caption = "Diego Álvarez Fernández") + 
                              theme_tufte()
max.var.curve.front.hist

max.var.curve.back <- sqldf("select `Max Variation Curve Back` as MaxVariationCurveBack, `Treatment` from eye_data")
max.var.curve.back <- filter(max.var.curve.back, MaxVariationCurveBack > 0)
max.var.curve.back.hist <- ggplot(max.var.curve.back, aes(x = MaxVariationCurveBack, fill = Treatment)) +
                              geom_histogram(binwidth = 0.1) +
                              labs(title="Histograma de las máximas desviaciones de las curvaturas de la \nzona anterior del ojo del paciente en función \ndel tratamiento dado", 
                                   caption = "Diego Álvarez Fernández") + 
                              theme_tufte()
max.var.curve.back.hist

#podemos estudiar los histogramas de las medias de las curvaturas en función del tratamiento

mean.curve.front <- sqldf("select `Mean Curve Front` as MeanCurveFront, `Treatment` from eye_data")
mean.curve.front <- filter(mean.curve.front, MeanCurveFront > 0)
mean.curve.front.hist <- ggplot(mean.curve.front, aes(x = MeanCurveFront, fill = Treatment)) + 
                            geom_histogram(binwidth = 0.1) +
                            labs(title="Histograma de las medias de las curvaturas de la \nzona posterior del ojo del paciente en función \ndel tratamiento dado", 
                                 caption = "Diego Álvarez Fernández") + 
                            theme_tufte()
mean.curve.front.hist

mean.curve.back <- sqldf("select `Mean Curve Back` as MeanCurveBack, `Treatment` from eye_data")
mean.curve.back <- filter(mean.curve.back, MeanCurveBack > 0)
mean.curve.back.hist <- ggplot(mean.curve.back, aes(x = MeanCurveBack, fill = Treatment)) + 
                            geom_histogram(binwidth = 0.1) +
                            labs(title="Histograma de las medias de las curvaturas de la \nzona anterior del ojo del paciente en función \ndel tratamiento dado", 
                                 caption = "Diego Álvarez Fernández") + 
                            theme_tufte()
mean.curve.back.hist

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
                      labs(title="Media de edades de los pacientes por el \ntratamiento indicado", 
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

#Lo mismo podemos hacer para estudiar la evolución de la paqui minima

paqui.per.treatment <- sqldf("select `Paqui Min` as PaquiMin, `Treatment` from eye_data")
paqui.per.treatment.density <- ggplot(paqui.per.treatment, aes(x = PaquiMin, fill = Treatment)) + 
  geom_density(alpha = 0.2) + 
  theme_tufte() + 
  labs(title="Gráfico de densidad de la distribución de paquimetría en \nfunción del tratamiento", 
       caption = "Diego Álvarez Fernández")
paqui.per.treatment.density

#podemos estudiar los dos parámetros que nos faltan

distance.per.treatment <- sqldf("select `Distance Between Max Curve and Min Paqui` as Distance, `Treatment` from eye_data")
distance.per.treatment.density <- ggplot(distance.per.treatment, aes(x = Distance, fill = Treatment)) + 
                                  geom_density(alpha = 0.2) + 
                                  theme_tufte() + 
                                  labs(title="Gráfico de densidad de la distribución de las distancias entre los puntos de máxima curvatura y mínima paquimetría en \nfunción del tratamiento", 
                                  caption = "Diego Álvarez Fernández")
distance.per.treatment.density

position.per.treatment <- sqldf("select `Position of Most Curve Point Relative to Center` as Position, `Treatment` from eye_data")
position.per.treatment.density <- ggplot(position.per.treatment, aes(x = Position, fill = Treatment)) + 
  geom_density(alpha = 0.2) + 
  theme_tufte() + 
  labs(title="Gráfico de densidad de la distribución de las distancias entre los puntos de máxima curvatura y mínima paquimetría en \nfunción del tratamiento", 
       caption = "Diego Álvarez Fernández")
position.per.treatment.density





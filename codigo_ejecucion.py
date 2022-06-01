#!/usr/bin/env python
# coding: utf-8

# # CODIGO DE EJECUCION

# *NOTA: Para poder usar este código de ejecución hay que lanzarlo desde exactamente el mismo entorno en el que fue creado.*
# 
# *Se puede instalar ese entorno en la nueva máquina usando el environment.yml que creamos en el set up del proyecto*
# 
# *Copiar el proyecto1.yml al directorio y en el terminal o anaconda prompt ejecutar:*
# 
# conda env create --file proyecto1.yml --name proyecto1

# In[23]:


import cloudpickle
import pandas as pd
from janitor import clean_names


def ejecutar_modelo(df):
    df.rename(columns = {'Temperature':'temperatura',
                         'Humidity':'humedad',
                         'Hours Since Previous Failure':'horas_desde_utlimo_fallo',
                         'Failure':'fallo'}, inplace=True)

    df.drop_duplicates(inplace = True)

    variables_finales = ['horas_desde_utlimo_fallo',
                         'humedad',
                         'temperatura']

    df = df[variables_finales].copy()

    nombre_pipe_ejecucion = 'pipe_ejecucion.pickle'

    ruta_pipe_ejecucion = nombre_pipe_ejecucion

    with open(ruta_pipe_ejecucion, mode='rb') as file:
       pipe_ejecucion = cloudpickle.load(file)

    pred = pipe_ejecucion.predict_proba(df)[:, 1]*100
    return(pred)


# In[ ]:





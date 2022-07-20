#!/usr/bin/env python
# coding: utf-8

# In[1]:


import altair as alt
#from vega_datasets import data
import pandas as pd
import numpy as np
from altair.expr import datum
import streamlit as st


# In[2]:


alt.data_transformers.disable_max_rows()


# In[3]:


data = pd.read_csv('almagro_cot.csv')


# In[ ]:


#data.columns

data1 = data.copy()
data1 = data1[data1['Tipo Unidad'] =='Departamento']
data1 = data[['N° Dormitorios','N° Baños','Comuna Proyecto','Precio de Venta en Uf Cotizacion','Metros Cuadrados','Estado Civil','Comuna Cliente', 'Edad', 'Programa']]
data1.columns = ['n_dormitorios', 'n_baños', 'comuna_proy', 'precio','m2','estado_civil','comuna_cli', 'edad','programa']
data1 = data1[data1.isna().sum(axis=1)==0]
data1['uf_m2'] = data1.precio/data1.m2
data1 = data1[data1.comuna_cli.isin(data1.comuna_cli.value_counts()[:10].index)]
data1 = data1[data1.uf_m2<200] 
data1 = data1[data1.estado_civil!='Empresa']


# In[ ]:


data1.loc[data1.programa.isin(['TRADICIONAL KC']), 'programa'] = 'Tradicional KC'
data1.loc[data1.programa.isin(['TRADICIONAL KA']), 'programa'] = 'Tradicional KA'
data1.loc[data1.programa.isin(['PENTHOUSE 2 PISOS','PENTHOUSE  2 PISOS','Penthouse 2']), 'programa'] = 'Penthouse 2 pisos'
data1.loc[data1.programa.isin(['Palomita']), 'programa'] = 'Paloma'
data1 = data1[data1.programa.isin(data1['programa'].value_counts()[:8].index)]


# In[4]:


data1.loc[data1.estado_civil.str.contains('Casado'), 'estado_civil'] = 'Casado(a)'
data1.loc[data1.estado_civil.str.contains('Union Civil'), 'estado_civil'] = 'Casado(a)'
data1.loc[data1.estado_civil.str.contains('Soltero'), 'estado_civil'] = 'Soltero(a)'
data1.loc[data1.estado_civil.str.contains('Separado'), 'estado_civil'] = 'Divorciado(a)'
data1.loc[data1.estado_civil.str.contains('0'), 'estado_civil'] = 'Sin información'


# In[5]:


selection = alt.selection_multi(fields=['programa', 'n_dormitorios'])
color = alt.condition(selection,
                      alt.Color('programa:N', legend=None),
                      alt.value('lightgray'))

stripplot =  alt.Chart(data1, width=40).mark_circle(size=8).encode(
    x=alt.X(
        'jitter:Q',
        title=None,
        axis=alt.Axis(values=[0], ticks=True, grid=False, labels=False),
        scale=alt.Scale(),
    ),
    y=alt.Y('uf_m2:Q'),
    color=color,
    column=alt.Column(
        'comuna_proy:N',
        header=alt.Header(
            labelAngle=-90,
            titleOrient='top',
            labelOrient='bottom',
            labelAlign='right',
            labelPadding=3,
        ),
    ),
).transform_calculate(
    # Generate Gaussian jitter with a Box-Muller transform
    jitter='sqrt(-2*log(random()))*cos(2*PI*random())'
).interactive()

legend = alt.Chart(data1).mark_rect().encode(
    y=alt.Y('programa:N', axis=alt.Axis(orient='right')),
    x='n_dormitorios:O',
    color=color
).add_selection(
    selection
).interactive()

st.title("Visualización preliminar proyecto")
stripplot | legend


st.altair_chart(stripplot.interactive(), use_container_width=True)


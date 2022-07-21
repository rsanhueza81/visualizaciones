#!/usr/bin/env python
# coding: utf-8


import altair as alt
import pandas as pd
import numpy as np
from altair.expr import datum
import streamlit as st



alt.data_transformers.disable_max_rows()
data = pd.read_csv('almagro_cot.csv')

data1 = data.copy()
data1 = data1[data1['Tipo Unidad'] =='Departamento']
data1 = data[['N° Dormitorios','N° Baños','Comuna Proyecto','Precio de Venta en Uf Cotizacion','Metros Cuadrados','Estado Civil','Comuna Cliente', 'Edad', 'Programa']]
data1.columns = ['n_dormitorios', 'n_baños', 'comuna_proy', 'precio','m2','estado_civil','comuna_cli', 'edad','programa']
data1 = data1[data1.isna().sum(axis=1)==0]
data1['uf_m2'] = data1.precio/data1.m2
data1 = data1[data1.comuna_cli.isin(data1.comuna_cli.value_counts()[:10].index)]
data1 = data1[data1.uf_m2<200] 
data1 = data1[data1.estado_civil!='Empresa']
data1.loc[data1.programa.isin(['TRADICIONAL KC']), 'programa'] = 'Tradicional KC'
data1.loc[data1.programa.isin(['TRADICIONAL KA']), 'programa'] = 'Tradicional KA'
data1.loc[data1.programa.isin(['PENTHOUSE 2 PISOS','PENTHOUSE  2 PISOS','Penthouse 2']), 'programa'] = 'Penthouse 2 pisos'
data1.loc[data1.programa.isin(['Palomita']), 'programa'] = 'Paloma'
data1 = data1[data1.programa.isin(data1['programa'].value_counts()[:8].index)]
data1.loc[data1.estado_civil.str.contains('Casado'), 'estado_civil'] = 'Casado(a)'
data1.loc[data1.estado_civil.str.contains('Union Civil'), 'estado_civil'] = 'Casado(a)'
data1.loc[data1.estado_civil.str.contains('Soltero'), 'estado_civil'] = 'Soltero(a)'
data1.loc[data1.estado_civil.str.contains('Separado'), 'estado_civil'] = 'Divorciado(a)'
data1.loc[data1.estado_civil.str.contains('0'), 'estado_civil'] = 'Sin información'
selection = alt.selection_multi(fields=['programa', 'n_dormitorios'])
color = alt.condition(selection,
                      alt.Color('programa:N', legend=None),
                      alt.value('lightgray'))

stripplot =  (alt.Chart(data1, width=40).mark_circle(size=8).encode(
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
).interactive())

legend = alt.Chart(data1).mark_rect().encode(
    y=alt.Y('programa:N', axis=alt.Axis(orient='right')),
    x='n_dormitorios:O',
    color=color
).add_selection(
    selection
).interactive()

st.title("Visualización preliminar proyecto")

#row1_1, row1_2 = st.columns((2, 3))

df2=data1[['Num_Operacion','Fecha Cotizacion','Nombre Proyecto','Nombre Etapa','Comuna Proyecto','Programa','Precio de Venta en Uf Cotizacion','Nombre_Propiedad','Modelo_Propiedad', 'Tipo Unidad',
       'Metros Cuadrados','N° Dormitorios','N° Baños','Fecha Reserva','Precio de Venta en UF Reserva','ID Cliente','Nombre Cliente','Comuna Cliente','Estado Civil','Edad','Profesion','TipoMedio']].copy()

df2.columns=['Id_cotizacion','Fecha_cotizacion','Nombre_proyecto','Nombre_etapa','Comuna_proyecto'
            ,'Programa_proyecto','Precio_cotizacion','Nombre_propiedad','Modelo_propiedad','Tipo_unidad','M2','N_dormitorios','N_banos',
            'Fecha_reserva','Precio_reserva','RUT_cliente','Nombre_cliente','Comuna_cliente','Estado_civil','Edad','Profesion','Origen_cotizacion']

m = df2.select_dtypes(np.number)
df2[m.columns]= m.round().astype('Int64')

#with row1_1:
st.header('Muestra de la data a utilizar:')
st.dataframe(df2.iloc[0:5])
#with row1_2:
st.write(
        """
    ##
    Examining how Uber pickups vary over time in New York City's and at its major regional airports.
    By sliding the slider on the left you can view different slices of time and explore different transportation trends.
    """
    )

stripplot | legend


#!/usr/bin/env python
# coding: utf-8


import altair as alt
import pandas as pd
import numpy as np
from altair.expr import datum
import streamlit as st


#st.set_page_config(layout="wide")
alt.data_transformers.disable_max_rows()

#####################################################################
############### LECTURA Y TRANSFORMACION DE DATOS ###################
#####################################################################
data = pd.read_csv('almagro_cot.csv')

data1 = data.copy()
data1 = data1[data1['Tipo Unidad'] =='Departamento']
data1 = data1[['N° Dormitorios','N° Baños','Comuna Proyecto','Precio de Venta en Uf Cotizacion','Metros Cuadrados','Estado Civil','Comuna Cliente', 'Edad', 'Programa','Fecha Reserva','Nombre Proyecto']]
data1.columns = ['n_dormitorios', 'n_baños', 'comuna_proy', 'precio','m2','estado_civil','comuna_cli', 'edad','programa','fecha_reserva','nombre_proyecto']

data1['n_dormitorios'] = data1.n_dormitorios.astype(int).astype(str)
data1['n_baños'] = data1.n_baños.astype(int).astype(str)

data1['reservado'] = 'No'
data1.loc[data1.fecha_reserva.notna(), 'reservado'] = 'Sí'
del data1['fecha_reserva']

data1 = data1[data1.isna().sum(axis=1)==0]
data1['uf_m2'] = data1.precio/data1.m2
data1 = data1[data1.uf_m2<200] 

data1.loc[data1.programa.isin(['TRADICIONAL KC']), 'programa'] = 'Tradicional KC'
data1.loc[data1.programa.isin(['TRADICIONAL KA']), 'programa'] = 'Tradicional KA'
data1.loc[data1.programa.isin(['PENTHOUSE 2 PISOS','PENTHOUSE  2 PISOS','Penthouse 2']), 'programa'] = 'Penthouse 2 pisos'
data1.loc[data1.programa.isin(['Palomita']), 'programa'] = 'Paloma'
data1 = data1[data1.programa.isin(data1['programa'].value_counts()[:8].index)]
#####################################################################
######################## VISUALIZACION 1 ############################
#####################################################################

data1=data1.sample(6000)
selection = alt.selection_single(fields=['reservado'])

color = alt.condition(selection,
                      alt.Color('reservado:N', legend=None, scale=alt.Scale(scheme='paired')),
                      alt.value('lightgray'))

stripplot =  alt.Chart(data1, width=40).mark_point().encode(
    x=alt.X(
        'jitter:Q',
        title=None,
        axis=alt.Axis(values=[0], ticks=True, grid=False, labels=False),
        scale=alt.Scale(),
    ),
    y=alt.Y('uf_m2:Q', title='UF por m2'),
    color=color,
    tooltip = 'nombre_proyecto',
    column=alt.Column(
        'comuna_proy:N',
        header=alt.Header(
            labelAngle=-90,
            title = 'Comuna proyecto',
            titleOrient='bottom',
            labelOrient='bottom',
            labelAlign='left',
            labelPadding=300-3
        ),
    ),
).transform_calculate(
    # Generate Gaussian jitter with a Box-Muller transform
    jitter='sqrt(-2*log(random()))*cos(2*PI*random())'
)

stripplot = stripplot.properties(title=alt.TitleParams(
    text="UF por m2 aperturado por comuna del proyecto",
    subtitle=["Inmobiliaria Almagro",""],
    fontSize=20,
    color='#3169A4',
    subtitleFontSize=16,
    subtitleColor="#525252",
    anchor="start"
        ),
    width=50,
    height=300)

legend = alt.Chart(data1).mark_bar().encode(
    y=alt.Y('count()', title='Cantidad cotizaciones'),
    x=alt.X('reservado:O', title='Reservado'),
    color=color
).add_selection(
    selection
)

programa_dropdown = alt.binding_select(options=[None] + list(data1.programa.unique()), labels = ['All'] + list(data1.programa.unique()), name="Programa")
programa_select = alt.selection_single(fields=['programa'], bind=programa_dropdown)

dormitorio_slider = alt.binding_select(options=[None] + list(sorted(data1.n_dormitorios.unique())), labels = ['All'] + list(sorted(data1.n_dormitorios.unique())), name="Dormitorios")
dormitorio_select = alt.selection_single(fields=['n_dormitorios'], bind=dormitorio_slider)

baño_slider = alt.binding_select(options=[None] + list(sorted(data1.n_baños.unique())), labels = ['All'] + list(sorted(data1.n_baños.unique())), name="Baños")
baño_select = alt.selection_single(fields=['n_baños'], bind=baño_slider)


stripplot = stripplot.add_selection(
    baño_select
).transform_filter(
    baño_select
).add_selection(
    dormitorio_select
).transform_filter(
    dormitorio_select
).add_selection(
    programa_select
).transform_filter(
    programa_select
)


legend = legend.add_selection(
    baño_select
).transform_filter(
    baño_select
).add_selection(
    dormitorio_select
).transform_filter(
    dormitorio_select
).add_selection(
    programa_select
).transform_filter(
    programa_select
)

################################################################################
############################## HTML ############################################
################################################################################
st.title("Visualización preliminar proyecto")

df2=data[['Num_Operacion','Fecha Cotizacion','Nombre Proyecto','Nombre Etapa','Comuna Proyecto','Programa','Precio de Venta en Uf Cotizacion','Nombre_Propiedad','Modelo_Propiedad', 'Tipo Unidad',
       'Metros Cuadrados','N° Dormitorios','N° Baños','Fecha Reserva','Precio de Venta en UF Reserva','ID Cliente','Nombre Cliente','Comuna Cliente','Estado Civil','Edad','Profesion','TipoMedio']].copy()

df2.columns=['Id_cotizacion','Fecha_cotizacion','Nombre_proyecto','Nombre_etapa','Comuna_proyecto'
            ,'Programa_proyecto','Precio_cotizacion','Nombre_propiedad','Modelo_propiedad','Tipo_unidad','M2','N_dormitorios','N_banos',
            'Fecha_reserva','Precio_reserva','RUT_cliente','Nombre_cliente','Comuna_cliente','Estado_civil','Edad','Profesion','Origen_cotizacion']

m = df2.select_dtypes(np.number)
df2[m.columns]= m.round().astype('Int64')

st.subheader('Muestra y descripción de la data')
st.write('**Muestra de la data:**')
st.dataframe(df2.iloc[0:5])
st.write("""Los datos a trabajar corresponden a cotizaciones de departamentos entre 2020 y 2021 en una importante empresa imobiliaria nacional. 
Se destacan cuatro familias de variables:
- **Datos relacionados con la cotización:** ID único, fecha cotización, precio mostrado en cotización, fecha reserva (si corresponde) , precio prometido en la reserva, canal de origen.
- **Datos relacionados con el proyecto:** Nombre, comuna, programa. 
- **Datos relacionados con el departamento:** Nombre, modelo, tipo, M2, número de dormitorios, números de baños.
- **Datos relacionados con el cliente:** Rut, Nombre, comuna de residencia, estado civil, edad, profesión """)

st.subheader('Prototipo de Idiom:')

values = st.slider(     'Select a range of values',1, 4, (1, 4),step=1)
st.write('Values:', data1.n_baños.min())

stripplot | legend

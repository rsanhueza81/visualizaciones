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
data1['fecha'] = pd.to_datetime(data['Fecha Cotizacion']).dt.to_period('M').astype(str)
data1['periodo'] = pd.to_datetime(data['Fecha Cotizacion']).dt.strftime('%b-%Y')

data1 = data1[['N° Dormitorios','N° Baños','Comuna Proyecto','Precio de Venta en Uf Cotizacion','Metros Cuadrados','Estado Civil','Comuna Cliente', 'Edad', 'Programa','Fecha Reserva','Nombre Proyecto','fecha','periodo']]
data1.columns = ['n_dormitorios', 'n_baños', 'comuna_proy', 'precio','m2','estado_civil','comuna_cli', 'edad','programa','fecha_reserva','nombre_proyecto','fecha','periodo']

data1['n_dorm']=data1.n_dormitorios.astype(int)
data1['n_dormitorios'] = data1.n_dormitorios.astype(int).astype(str)
data1['n_banos']=data1.n_baños.astype(int)
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

st.subheader('Precios de cotización y venta por comuna')

#####################################################################
######################## VISUALIZACION 1 ############################
#####################################################################

data_v1=data1.sample(6000,random_state=3).copy()

programas=list(data1.programa.unique())
tipos_dpto = st.multiselect('Selecciona el tipo de departamento:', programas ,programas)

col1, col2 = st.columns(2)

with col1:
       slider_banos = st.slider('Número de baños',1, 4, (1,4),step=1)
with col2:
       slider_dormitorios = st.slider('Número de dorm',1, 5, (1,5),step=1)

data_v1=data_v1[ (data_v1['n_banos']>=slider_banos[0]) & (data_v1['n_banos']<=slider_banos[1])]
data_v1=data_v1[(data_v1['n_dorm']>=slider_dormitorios[0]) & (data_v1['n_dorm']<=slider_dormitorios[1])]
data_v1=data_v1[data_v1.programa.isin(tipos_dpto)]

########### ALTAIR CODE ################
selection = alt.selection_single(fields=['reservado'])

color = alt.condition(selection,
                      alt.Color('reservado:N', legend=None, scale=alt.Scale(range=['#AECDE1','#EC5A53'])),
                      alt.value('lightgray'))

stripplot =  alt.Chart(data_v1, width=40).mark_point().encode(
    x=alt.X(
        'jitter:Q',
        title=None,
        axis=alt.Axis(values=[0], ticks=True, grid=False, labels=False),
        scale=alt.Scale(),
    ),
    y=alt.Y('uf_m2:Q', title='UF por m2 sobre el precio'),
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

stripplot = stripplot.properties(width=50,
    height=300)

legend = alt.Chart(data_v1).mark_bar().encode(
    y=alt.Y('count()', title='Cantidad cotizaciones'),
    x=alt.X('reservado:O', title='Reservado'),
    color=color
).add_selection(
    selection
)

########### ALTAIR CODE ################

if len(tipos_dpto)==0:
       st.subheader('No hay cotizaciones para los filtros seleccionados')
else:
       stripplot | legend

       
       
################### VIZUALIZACION 2 ######################################
st.subheader('Precios de cotización y venta por comuna')


comunas=list(data1.comuna_proy.unique())
comunas2=['Ver todo']+comunas
proyectos=list(data1.nombre_proyecto.unique())
proyectos2=['Ver todo']+proyectos
dict_proy = {}
for comuna in data1.comuna_proy.unique():
       dict_proy[comuna] = list(data1[data1.comuna_proy==comuna].nombre_proyecto.unique())
col3, col4 = st.columns([1,3])

with col3:
       selector_comuna = st.selectbox('Selecciona la comuna a revisar',comunas2)

       if selector_comuna=='Ver todo':
               filtro_comuna=comunas
               bool_proyecto=True
               proyecto_com=proyectos2

       if selector_comuna!='Ver todo':
               bool_proyecto=False
               filtro_comuna=[selector_comuna]
               proyecto_com=['Comuna completa']+dict_proy[selector_comuna]


       

       selector_proyecto = st.selectbox('Selecciona el proyecto a revisar',proyecto_com,disabled=bool_proyecto)

       if selector_proyecto=='Ver todo':
           filtro_proyectos=proyecto_com

       elif selector_proyecto=='Comuna completa':
           filtro_proyectos=proyecto_com

       else:# selector_proyecto!='Ver todo':
           filtro_proyectos=[selector_proyecto]


       magnitud = st.radio("¿Qué quiere medir?",['cantidad', 'monto'])

######################## ALTAIR ###################################
data_v2 = data1.copy()
data_v2['reservado2'] = 0

# filtros william
data_v2=data_v2[data_v2.comuna_proy.isin(filtro_comuna)]
data_v2=data_v2[data_v2.nombre_proyecto.isin(filtro_proyectos)]


data_v2.loc[data_v2.reservado=='Sí', 'reservado2']=1
data_v2['monto'] = (data_v2.precio * data_v2.reservado2).astype(int)
data_v2 = data_v2.groupby(['fecha','periodo']).agg({'reservado2':['count','sum'],'monto':['sum'],'precio':['sum']}).reset_index()
data_v2.columns = ['fecha','periodo','cantidad','reservas','monto','monto_total']
data_v2['tasa_cantidad'] = data_v2.reservas/data_v2.cantidad
data_v2['tasa_monto'] = data_v2.monto/data_v2.monto_total
data_v2['fecha']=data_v2.fecha.astype(str)

if magnitud=='cantidad':
    title_y1 = 'Cantidad Cotizaciones'
    title_y2 = 'Tasa Cotizaciones Concretadas'
elif magnitud=='monto':
    title_y1 = 'Monto Total (UF)'
    title_y2 = 'Tasa Monto Concretado'

with col4:
       base = alt.Chart(data_v2).encode(alt.X('fecha:O', title=None))

       bar = base.mark_bar(color='#AECDE1').encode(alt.Y(f'{magnitud}:Q',
                                    axis=alt.Axis(title=title_y1, 
                                                  titleColor='#98B2C5',
                                                  titleFontSize=14)),
                                    tooltip=[
                                        alt.Tooltip('cantidad', title='Cantidad cotizaciones'),
                                        alt.Tooltip('tasa_cantidad', format='.1%',title='Tasa cot. concretadas'),
                                        alt.Tooltip('monto', title='Monto total'),
                                        alt.Tooltip('tasa_monto', format='.1%', title='Tasa monto concretado'),
                                    ]).interactive()

       line =  base.mark_line(point=alt.OverlayMarkDef(color="#EC5A53"),color='#EC5A53').encode(alt.Y(f'tasa_{magnitud}:Q',
                                    axis=alt.Axis(title=title_y2, 
                                                  titleColor='#EC5A53',
                                                  titleFontSize=14,
                                                  format='%')),
                                    tooltip=[
                                        alt.Tooltip('cantidad', title='Cantidad cotizaciones'),
                                        alt.Tooltip('tasa_cantidad', format='.1%',title='Tasa cotizaciones concretadas'),
                                        alt.Tooltip('monto', title='Monto total'),
                                        alt.Tooltip('tasa_monto', format='.1%', title='Tasa monto concretado'),
                                    ]).interactive()
       chart = alt.layer(bar, line).resolve_scale(
           y = 'independent'
       )

       chart=chart.properties(width=800,height=400)
       chart

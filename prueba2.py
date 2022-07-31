import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image

import altair as alt
import pandas as pd
import numpy as np
from altair.expr import datum



#st.set_page_config(layout="wide")
alt.data_transformers.disable_max_rows()

#####################################################################
############### LECTURA Y TRANSFORMACION DE DATOS ###################
#####################################################################
data = pd.read_csv('almagro_cot.csv')

data1 = data.copy()
data1['fecha'] = pd.to_datetime(data['Fecha Cotizacion']).dt.to_period('M').astype(str)
data1['periodo'] = pd.to_datetime(data['Fecha Cotizacion']).dt.strftime('%b-%Y')
data1 = data1[data1['Tipo Unidad'] =='Departamento']
data1 = data1[['N° Dormitorios','N° Baños','Comuna Proyecto','Precio de Venta en Uf Cotizacion','Metros Cuadrados','Estado Civil','Comuna Cliente', 'Edad', 'Programa','Fecha Reserva','Nombre Proyecto','fecha','periodo']]
data1.columns = ['n_dormitorios', 'n_baños', 'comuna_proy', 'precio','m2','estado_civil','comuna_cli', 'edad','programa','fecha_reserva','nombre_proyecto','fecha','periodo']

data1['n_dorm']=data1.n_dormitorios.astype(int)
data1['n_banos']=data1.n_baños.astype(int)
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



with st.sidebar:
    choose = option_menu("Proyecto Visualización de la Información. Análisis Comercial Inmobiliario", ["Contexto y usuarios", "Datos", "Tareas", "Visualizaciones"],
                         icons=['people-fill', 'table', 'list-task', 'file-bar-graph'],
                         menu_icon="building", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "20px"}, 
        "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#02ab21"},
    }
    )

if choose == "Contexto y usuarios":
    
    st.title("Contexto y usuarios")
    st.write("En encuentro  de ejecutivos del área comercial de inmobiliaria líder en Chile desean analizar estrategia de precios a establecer en los  próximos meses.")
    st.write("El objetivo que guía el encuento es poder establecer relación entre precios de departamentos medido en UF/m2 y los mercados donde se establecen los proyectos. Asimismo es importante establecer tendencias en cuento a la demanda , medido en cotizaciones de productos, y la forma en que esta demanda se concreta en operaciones de venta.")
    
    
    image = Image.open('almagro.jpg')
    st.image(image )
    
if choose == "Datos":
    df2=data[['Num_Operacion','Fecha Cotizacion','Nombre Proyecto','Nombre Etapa','Comuna Proyecto','Programa','Precio de Venta en Uf Cotizacion','Nombre_Propiedad','Modelo_Propiedad', 'Tipo Unidad',
       'Metros Cuadrados','N° Dormitorios','N° Baños','Fecha Reserva','Precio de Venta en UF Reserva','Comuna Cliente','Estado Civil','Edad','Profesion','TipoMedio']].copy()

    df2.columns=['Id_cotizacion','Fecha_cotizacion','Nombre_proyecto','Nombre_etapa','Comuna_proyecto'
            ,'Programa_proyecto','Precio_cotizacion','Nombre_propiedad','Modelo_propiedad','Tipo_unidad','M2','N_dormitorios','N_banos',
            'Fecha_reserva','Precio_reserva','Comuna_cliente','Estado_civil','Edad','Profesion','Origen_cotizacion']

    m = df2.select_dtypes(np.number)
    df2[m.columns]= m.round().astype('Int64')

    st.title('Muestra y descripción de la data')
    st.write('**Muestra de la data:**')
    st.dataframe(df2.iloc[0:5])
    st.write("Los datos a trabajar corresponden a cotizaciones de departamentos entre 2019 y 2022 en una importante empresa imobiliaria nacional.")
    
    st.write("Se destacan cuatro familias de variables:")
    
    st.write("-Datos relacionados con la cotización: ID único, fecha cotización, precio mostrado en cotización, fecha reserva (si corresponde) , precio prometido en la reserva, canal de origen.")
    st.write("-Datos relacionados con el proyecto: Nombre, comuna, programa.")
    st.write("-Datos relacionados con el departamento: Nombre, modelo, tipo, M2, número de dormitorios, números de baños.")
    st.write("-Datos relacionados con el cliente: comuna de residencia, estado civil, edad, profesión.")
    
if choose == "Tareas":
    
    st.title("Tareas de Visualización")
    st.write("Se han identificado las dos siguientes tareas de visualización las cuales serán aboradadadas en sus respectivos idioms:")
    st.write(" -Presentar la relación existente entre el precio de los departamentos comercializados por la Inmobiliaria y la localización de sus respectivos proyectos (comunas).")
    st.write(" -Presentar la evolución en la demanda de productos  de la inmobiliaria y su tasa de concreción en negocios (promesas de compra venta).")
    
    
    imagedos = Image.open('almagro2.jpg')
    st.image(imagedos)
    
if choose == "Visualizaciones":
    
    
    
    
    
######################################################################
################ PRIMERA VIZUALIZACION ###############################
######################################################################
    st.title("Visualizaciones")
          
################### VIZUALIZACION 1 ######################################
    st.subheader('Evolución volumen de cotizaciones y tasas de concreción')
    st.text("Tasas de concreción medida como ventas/cotizaciones en periodo")
    ######################## CODIGO SELECTORES ###################################

    comunas=list(data1.comuna_proy.unique())
    comunas2=['Ver todo']+comunas
    proyectos=list(data1.nombre_proyecto.unique())
    proyectos2=['Ver todo']+proyectos
    dict_proy = {}
    for comuna in data1.comuna_proy.unique():
           dict_proy[comuna] = list(data1[data1.comuna_proy==comuna].nombre_proyecto.unique())
    col3, col4 = st.columns([1,3])

    with col3:
           magnitudes = st.radio("¿Qué quiere medir?",['Cantidad', 'Monto (UF)'])
           if magnitudes=='Cantidad':
                  magnitud='cantidad'
           if magnitudes=='Monto (UF)':
                  magnitud='monto'

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


    ######################## CODIGO GRAFICOS ###################################
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
        title_y2 = 'Tasa concreción cotizaciones'
    elif magnitud=='monto':
        title_y1 = 'Monto Total (UF)'
        title_y2 = 'Tasa concreción cotizaciones'

    with col4:
           base = alt.Chart(data_v2).encode(alt.X('fecha:O', title=None))

           bar = base.mark_bar(color='#AECDE1').encode(alt.Y(f'{magnitud}:Q',
                                        axis=alt.Axis(title=title_y1, 
                                                      titleColor='#98B2C5',
                                                      titleFontSize=14)),
                                        tooltip=[
                                            alt.Tooltip('cantidad', title='Cantidad cotizaciones'),
                                            alt.Tooltip('tasa_cantidad', format='.1%',title='Tasa concreción cotizaciones'),
                                            alt.Tooltip('monto', title='Monto total'),
                                            alt.Tooltip('tasa_monto', format='.1%', title='Tasa concreción cotizaciones'),
                                        ]).interactive()

           line =  base.mark_line(point=alt.OverlayMarkDef(color="#EC5A53"),color='#EC5A53').encode(alt.Y(f'tasa_{magnitud}:Q',
                                        axis=alt.Axis(title=title_y2, 
                                                      titleColor='#EC5A53',
                                                      titleFontSize=14,
                                                      format='%')),
                                        tooltip=[
                                            alt.Tooltip('cantidad', title='Cantidad cotizaciones'),
                                            alt.Tooltip('tasa_cantidad', format='.1%',title='Tasa concreción cotizaciones'),
                                            alt.Tooltip('monto', title='Monto total'),
                                            alt.Tooltip('tasa_monto', format='.1%', title='Tasa concreción cotizaciones'),
                                        ]).interactive()
           chart = alt.layer(bar, line).resolve_scale(
               y = 'independent'
           )

           chart=chart.properties(width=600,height=400)
           chart

######################################################################
################ SEGUNDA VIZUALIZACION ###############################
######################################################################  
    st.subheader("Precio de cotizaciones (UF/m2) aperturado por comuna y estado (reservado/no reservado)")
    data_v1=data1.sample(6000,random_state=3).copy()

    programas=list(data1.programa.unique())
    tipos_dpto = st.multiselect('Selecciona el tipo de departamento:', programas ,programas)

    col1, col2 = st.columns(2)

    with col1:
           slider_banos = st.slider('Número de baños:',1, 4, (1,4),step=1)
    with col2:
           slider_dormitorios = st.slider('Número de dormitorios:',1, 5, (1,5),step=1)

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
        y=alt.Y('uf_m2:Q', title='UF por m2 sobre el precio cotizado'),
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

        jitter='sqrt(-2*log(random()))*cos(2*PI*random())'
    )

    stripplot = stripplot.properties(width=50,
        height=300)

    legend = alt.Chart(data_v1).mark_bar().encode(
        y=alt.Y('count()', title='Cantidad cotizaciones'),
        x=alt.X('reservado:O', title='Reserva concretada'),
        color=color
    ).add_selection(
        selection
    )


    if len(tipos_dpto)==0:
           st.write('No hay cotizaciones para los filtros seleccionados')
    else:
           stripplot | legend
 

    
   
    
    
    

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



with st.sidebar:
    choose = option_menu("Proyecto Visualización de la Información", ["Contexto y usuarios", "Datos", "Tareas", "Visualizaciones"],
                         icons=['people-fill', 'table', 'list-task', 'file-bar-graph'],
                         menu_icon="building", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
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
    st.write("Los datos a trabajar corresponden a cotizaciones de departamentos entre 2020 y 2021 en una importante empresa imobiliaria nacional.")
    
    st.write("Se destacan cuatro familias de variables:")
    
    st.write("-Datos relacionados con la cotización: ID único, fecha cotización, precio mostrado en cotización, fecha reserva (si corresponde) , precio prometido en la reserva, canal de origen.")
    st.write("-Datos relacionados con el proyecto: Nombre, comuna, programa.")
    st.write("-Datos relacionados con el departamento: Nombre, modelo, tipo, M2, número de dormitorios, números de baños.")
    st.write("-Datos relacionados con el cliente: comuna de residencia, estado civil, edad, profesión.")

    
   
    
    
    

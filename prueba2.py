import streamlit as st
from streamlit_option_menu import option_menu

with st.sidebar:
    choose = option_menu("Proyecto Visualización", ["Contexto y usuarios", "Datos", "Tareas", "Visualizaciones"],
                         icons=['people-fill', 'table', 'list-task', 'file-bar-graph'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#02ab21"},
    }
    )

if choose == "Contexto y usuarios":
    
    st.title("Contexto y usuarios")
    st.text("En encuentro  de ejecutivos del área comercial de inmobiliaria líder en Chile desean analizar estrategia de precios a establecer en los  próximos meses")
    st.text("El objetivo que guía el encuento es poder establecer relación entre precios de departamentos medido en UF/m2 y los mercados donde se establecen los proyectos. Asimismo es importante establecer tendencias en cuento a la demanda , medido en cotizaciones de productos, y la forma en que esta demanda se concreta en operaciones de venta")
    
   
    
    
    

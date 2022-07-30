import streamlit as st
from streamlit_option_menu import option_menu

with st.sidebar:
    choose = option_menu("Proyecto Visualización", ["Contexto", "Datos", "Tareas", "Visualizaciones"],
                         icons=['house', 'camera fill', 'kanban', 'book'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#02ab21"},
    }
    )

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
    st.text("en un encuentro anual")
    st.set_page_config(layout="wide")

   
    st.markdown('<p class="big-font">Hello World !!</p>', unsafe_allow_html=True)
    
    
    

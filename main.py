import os
import streamlit as st
st.set_page_config(initial_sidebar_state="collapsed",layout="wide", page_icon=":popcorn:")
from streamlit_navigation_bar import st_navbar
import pages as pg

# Removed one of the calls to st.set_page_config()


pages = ["Hệ thống gợi ý phim", "Khai phá dữ liệu"]
parent_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(parent_dir, "logo.svg")

styles = {
    "nav": {
        "background-color": "#2e2e39",
        "justify-content": "left",
    },
    "img": {
        "padding-right": "14px",
    },
    "span": {
        "color": "white",
        "width":"500px"
    },
    "active": {
        "color": "var(--text-color)",
        "font-weight": "normal",
        "color": "white",
    },
}

options = {
    "show_menu": False,
    "show_sidebar": False,
}

page = st_navbar(
    pages,
    logo_path=logo_path,
    styles=styles,
    options=options,
)

st.markdown("""
<style>
[data-testid="stAppSidebar"] {display: none;visibility: hidden;}
[data-testid="stHeader"] {display: none;}
</style>
""", unsafe_allow_html=True)



st.markdown("""
<style>
[data-testid="StyledLinkIconContainer"] {color:white;}
[data-testid="stMarkdownContainer"]  {color:white;}

[data-testid="stImage"] {width: 900px;}
</style>
""", unsafe_allow_html=True)

background_image = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
    background-image: url("https://repository-images.githubusercontent.com/275336521/20d38e00-6634-11eb-9d1f-6a5232d0f84f");
    background-size: cover;  
    background-position: center;  
}}
</style>
"""

st.markdown(background_image, unsafe_allow_html=True)


functions = {
    "Hệ thống gợi ý phim": pg.show_home,
    "Khai phá dữ liệu": pg.show_EDA,
}
go_to = functions.get(page)
if go_to:
    go_to() 

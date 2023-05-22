import streamlit as st
import time
from streamlit_option_menu import option_menu

import base64


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover;
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('bg.png')    


selected=option_menu(

    menu_title=None,
    options=["Main","Investment Tracker","Contact"],  
    icons=["house",'currency-dollar','envelope'],
    default_index=0,
    menu_icon="menu-button-wide" , 
    orientation='horizontal',
    
)
if selected=="Main":
   
    with open("app.py") as f:
        exec(f.read())
if selected=="Contact":
    
   
    st.subheader("Tushar Anand")
    st.subheader("2022B3PS1371H")
    st.subheader("anand.tushar2010@gmail.com")

if selected=="Investment Tracker":
    
    with open("invst_trckr.py") as f:
        exec(f.read())



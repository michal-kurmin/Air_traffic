import streamlit as st
import os
from etl import load_all_data

st.set_page_config(
    page_title="Air Traffic Analytics",
    page_icon="",
    layout="wide",  # Use wide layout
)

def load_all_data_if_not_exists():
    file_path = "flights.csv"
        
    if os.path.exists(file_path):
        st.write("Data already loaded")
    else:
        st.write("No data - importing from azure storage blob - please be patient")
        load_all_data()
        st.write("All data imported")

def load_page():
    # Add the image
    st.image("chartplane.jpg",use_container_width=True)
    # Add text over the image
    st.markdown(
        """
        <style>
        .title {
            position: relative;
            top: -800px; /* Adjust this value to move the text up or down */
            text-align: center;
            font-size: 52px;
            color: black;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }
        .footer {
            position: relative;
            top: -200px; /* Adjust this value to move the text up or down */
            text-align: center;
            font-size: 36px;
            color: black;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }
        </style>
        <div class="title">Analysis of commercial flights based on data from EUROCONTROL</div>
        """,
        unsafe_allow_html=True
    )
    
    # Add text at the bottom
    st.markdown(
        """
        <div class="footer"> Diploma project by Michal and Kasia under the supervision of Dr. Krzysztof Ziolkowski</div>
        """,
        unsafe_allow_html=True
    )
    
       
    st.markdown(
        """
        Data sources:
        
        - **Air Traffic Data**: EUROCONTROL
        - **Airport Codes**: [Airport Codes Database](#)
        - **Aircraft Database**: [Gigasheet](https://www.gigasheet.com)
        """
    )


load_all_data_if_not_exists()
load_page()
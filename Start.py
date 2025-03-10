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
    if os.path.exists('status.txt'):
        with open('status.txt', 'r') as file:
            status = file.read().strip()
        if status=='start':
            st.write("Last import not finished - importing data from azure storage blob - please be patient")
            load_all_data()
            st.write("All data imported")
        if status=='finished':
            if os.path.exists(file_path):
                st.write("")
            else:
                st.write("No data - importing from azure storage blob - please be patient")
                with open('status.txt', 'w') as file:
                    file.write('start')
                load_all_data()
                st.write("All data imported")
        if status not in ['start','finished']:
            st.write('Error')
    else:
        st.write("No data - importing from azure storage blob - please be patient")
        with open('status.txt', 'w') as file:
            file.write('start')
        load_all_data()
        st.write("All data imported")

def load_page():
    st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
            padding-left: 5rem;
            padding-right: 5rem;
        }
        h1 {
            text-align: center;
        }
        h2 {
            text-align: center;
        }
    </style>
    """, unsafe_allow_html=True)


    # Add the image

    st.title("Analysis of commercial flights based on data from Eurocontrol")



    st.image("chartplane.jpg",use_container_width=True)
    st.header("Diploma project by Michal Kurmin and Kasia Sandej under the supervision of Dr. Krzysztof Ziolkowski")
 
       
    st.markdown(
        """
        Data sources:
        
        - **Air Traffic Data**: [EUROCONTROL](https://www.eurocontrol.int/)
        - **Airport Codes**: [DataHub](https://datahub.io/)
        - **Aircraft Database**: [Gigasheet](https://www.gigasheet.com)
        """
    )

    st.markdown("""
The ATM Dataset should only be used for research and development.
The ATM Dataset should not be shared or distributed.
EUROCONTROL should be duly acknowledged as the source of the ATM Dataset.
It is acknowledged and accepted that EUROCONTROL provides the ATM Dataset as-is, without warranties of any kind.
""")
load_all_data_if_not_exists()
load_page()
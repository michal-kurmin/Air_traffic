import streamlit as st
from etl import check_for_new_csv, load_all_data

st.title("Update data")
st.write("Checking if there is new data on azure storage blob")

new_data=check_for_new_csv()

st.write(new_data)

if new_data=="New data available":
    st.write("Do you want to download new data?")
    # Add a button to the Streamlit app
    if st.button("Update data"):
        # Action to perform when the button is pressed
        st.write("Loading data  - importing from azure storage blob - please be patient")
        load_all_data()
        st.write("Data loaded")
elif new_data=="No new data":
    st.write("Do you want to udownload the same data again?")
    # Add a button to the Streamlit app
    if st.button("Download data again"):
        # Action to perform when the button is pressed
        st.write("Loading data  - importing from azure storage blob - please be patient")
        load_all_data()
        st.write("Data loaded")

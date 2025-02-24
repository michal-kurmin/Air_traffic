import streamlit as st
from etl import check_for_new_csv, load_all_data
import os

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

st.write("")
st.header("Update data")
st.write("")
st.write("Checking if there is new data on azure storage blob")
new_data = check_for_new_csv()

st.write(new_data)

update_password = st.text_input("Please input password for data update", type="password")

def perform_update():
    env_pass = os.environ.get("UPDATE_PASS")
    
    if env_pass is None:
        st.error("Environment variable 'UPDATE_PASS' is not set. Please configure it in your Azure app settings.")
        return
    
    if update_password == env_pass:
        try:
            st.info("Loading data - importing from Azure Storage Blob - please be patient")
            load_all_data()
            st.success("Data loaded successfully")
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
    elif update_password:  # Only show error if password was actually entered
        st.error("Wrong password")

if new_data == "New data available":
    st.write("Do you want to download new data?")
    if st.button("Update data"):
        perform_update()
elif new_data == "No new data":
    st.write("Do you want to download the same data again?")
    if st.button("Download data again"):
        perform_update()
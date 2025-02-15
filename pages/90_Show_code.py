import streamlit as st

# Streamlit app title
st.title("Show code")
st.write("Please choose code you want to see")

# List of options for the dropdown
options = ['Choose page/modul to dispaly code','ETL', 'Start', 'Busiest Airports', 'Average delay','Packages']

# Create a dropdown list
selected_option = st.selectbox("Select code to show:", options)

def display_code(file_name):
    with open(file_name, 'r') as file:
        # Read the entire file content
        content = file.read()
    
    # Print the content
    st.write(f'File: {file_name}')
    st.code(content, language="python", line_numbers=True, wrap_lines=True)
    
    
if selected_option=="Choose page/modul to dispaly code":
    st.write("No page selected") 
# =============================================================================
#     st.markdown("""
# <pre style="font-family:monospace; white-space:pre">
# streamlit_app/
# ├── README.md        # Project documentation
# ├── requirements.txt # Project dependencies
# ├── .gitignore       # Git ignore file
# ├── Start.py         # Main Streamlit application
# ├── etl.py           # Load data from azure, clean, and prepare data for pages
# ├── df_for_pages     # Read prepared csv and return df
# ├── chartplane.jpg   # Image for Start,py
# │
# ├── pages/               # Additional pages for multi-page apps
# │   ├── 1_Busiest_airports.py
# │   ├── 2_Covid_impact
# │   ├── 
# │   ├── page1.py
# │   └── page2.py
# │
# ├── data/                   # Data files
# │  
# └── .streamlit/config.toml  #stemlit config
# </pre>
# """, unsafe_allow_html=True)
# 
# =============================================================================
    
if selected_option=="ETL":
    # Specify the file path
    display_code("etl.py")
    
if selected_option=="main":
    # Specify the file path
    display_code("start.py")
    
if selected_option=="Busiest Airports":
    # Specify the file path
    display_code("pages/1_Busiest_airports.py")

if selected_option=="Average delay":
    # Specify the file path
    display_code("pages/3_Average_delay.py")

if selected_option=="Packages":
    # Specify the file path
    display_code("requirements.txt")
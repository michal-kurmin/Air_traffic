import streamlit as st

# Streamlit app title
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
st.header("Display code of modules and pages")
# List of options for the dropdown
options = ['Choose page/modul to dispaly code',
           'ETL',
           'Start',
           'Busiest Airports',
           'Covid impact',
           'Delayed flights',
           'Planes and distances',
           'DataFrames for analytics',
           'Update data',
           'Show code',
           'Packages']

# Create dropdown list
selected_option = st.selectbox("Select code to show:", options)

# Function to display the code of selected page
def display_code(file_name):
    with open(file_name, 'r') as file:
        content = file.read()
    # Print the content
    st.header(f'File: {file_name}')
    st.code(content, language="python", line_numbers=True, wrap_lines=True)
    
    
if selected_option=="Choose page/modul to dispaly code":
    st.write("No page selected") 
    st.code("""
    streamlit_app/
    ├── README.md                       # Project documentation
    ├── requirements.txt                # Project dependencies
    ├── .gitignore                      # Git ignore file
    ├── Start.py                        # Main Streamlit application
    ├── etl.py                          # Load data from azure, clean, and prepare data for pages
    ├── df_for_pages                    # Read prepared csv and return df
    ├── chartplane.jpg                  # Image for Start,py
    │
    ├── pages/                          # Additional pages for multi-page apps
    │   ├── 1_Busiest_airports.py       # Airports traffic analytics
    │   ├── 2_Covid_impact.py           # Traffic time analytics
    │   ├── 3_Delayed_flights.py        # Delayed flights analysis
    │   ├── 4_Planes_and_distances.py   # Planes and distances analysis
    │   ├── 80_Update_data.py           # Checking for data updates/updating data
    │   └── 90_Show_code.py             # Dispaying python code (current page)
    │
    ├── data/                           # Data files
    │
    └── .streamlit/config.toml          #stremlit config

    """, )
    
if selected_option=="ETL":
    # Specify the file path
    display_code("etl.py")
    
if selected_option=="Start":
    # Specify the file path
    display_code("Start.py")
    
if selected_option=="Busiest Airports":
    # Specify the file path
    display_code("pages/1_Busiest_airports.py")

if selected_option=="Delayed flights":
    # Specify the file path
    display_code("pages/3_Delayed_flights.py")

if selected_option=="Planes and distances":
    # Specify the file path
    display_code("pages/4_Planes_and_distances.py")

if selected_option=="Packages":
    # Specify the file path
    display_code("requirements.txt")

if selected_option=="Covid impact":
    # Specify the file path
    display_code("pages/2_Covid_impact.py")

if selected_option=="DataFrames for analytics":
    # Specify the file path
    display_code("df_for_pages.py")

if selected_option=="Update data":
    # Specify the file path
    display_code("pages/80_Update_data.py")

if selected_option=="Show code":
    # Specify the file path
    display_code("pages/90_Show_code.py")
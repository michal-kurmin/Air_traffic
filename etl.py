import pandas as pd
from azure.storage.blob import BlobServiceClient
from io import StringIO
import streamlit as st
import os

def load_data_from_blob():
    # If exists deleting flights.csv
    file_path = 'flights.csv'
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"File {file_path} deleted successfully.")
        except FileNotFoundError:
            print(f"File {file_path} does not exist.")
        except PermissionError:
            print(f"Permission denied: Unable to delete {file_path}.")
        except Exception as e:
            print(f"Error occurred while deleting file {file_path}: {e}")
    
    # Connection string to our blob
    connection_string = os.environ["BLOB_CONNECTION_STRING"]

    # Create a BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    
    df=pd.DataFrame()
    
    # Specify the container name
    container_name = "csv-data"
    container_client = blob_service_client.get_container_client(container_name)
     
    # Include only columns which we will use later
    columns_to_include = ['ADEP',  
                          'ADES',
                          'FILED OFF BLOCK TIME',
                          'FILED ARRIVAL TIME', 
                          'ACTUAL OFF BLOCK TIME', 
                          'ACTUAL ARRIVAL TIME',
                          'AC Type', 
                          'AC Operator', 
                          'ICAO Flight Type',       
                          'STATFOR Market Segment',  
                          'Actual Distance Flown (nm)']
    # Colums which we exclude: ['ECTRL ID','ADEP Latitude', 'ADEP Longitude',
    #'ADES Latitude', 'ADES Longitude','AC Registration','Requested FL']
    i=0
    try:
        # List blobs in the container
        blob_list = container_client.list_blobs()
        for blob in blob_list:
            # Download the blob content as a string
            st.write('loading csv',i)
            i+=1
            blob_client = container_client.get_blob_client(blob)
            blob_data = blob_client.download_blob().content_as_text()
            
            # Convert the string data to a DataFrame
            df = pd.read_csv(StringIO(blob_data),usecols=columns_to_include)
            clean_chunk(df)
    except Exception as e:
        st.write(f"Failed to load CSV files: {e}")
    
    # Specify the file path to write number of csv files loaded
    file_path = "number.txt"
    
    # Open the file in write mode and write the integer as a string
    with open(file_path, 'w') as file:
        file.write(str(i))
    return 

def clean_chunk(df):
    # Drop rows with NaN values
    df = df.dropna()
    
    # Drop rows with empty strings
    df = df[~(df == '').any(axis=1)]
    
    #filter for regular planes (no helicopters etc)
    #read data about aircrafts
    aircraftDB = pd.read_csv('aircraft_types.csv') 
    conventional_airplanes = aircraftDB[aircraftDB['AircraftDescription'] == 'LandPlane']
    # Get unique values from the 'Description' column and convert to a list
    conventional_airplanes_list = conventional_airplanes['Designator'].unique().tolist()
    df=df[df['AC Type'].isin(conventional_airplanes_list)]
    
    #filtering only jets and turboprop planes (other are used mainly as a
    #touristi or private planes
    jet_airplanes = aircraftDB[aircraftDB['EngineType'].isin(['Jet', 'Turboprop/Turboshaft'])]
    jet_airplanes_list=jet_airplanes['Designator'].unique().tolist()
    df=df[df['AC Type'].isin(jet_airplanes_list)]
    
    #we exclude flights with special codes ZZZZ or AFIL ((landing site without code or plan filled in air ))  
    for col in ['ADEP','ADES']:
        df=df[~df[col].isin(['AFIL','ZZZZ'])]
    
    #data for 2022 september and december there is no data about segment
    #we won't be able to use for segment analysis, but this data is still 
    #for whole air traffic analysis
    
    # Saving to csv(no columns if file exists, with columns if doesn't)
    if os.path.exists('flights.csv'):
        df.to_csv('flights.csv', mode='a', header=False, index=False)
    else:
        #Changing columns names for more user friendly
        new_column_names =['dep_airport', 'arr_airport', 'plan_dep', 'plan_arr',
               'real_dep', 'real_arr', 'plane_type',
               'operator', 'fligt_type', 'segment',
               'real_distance']
        df.columns=new_column_names
        df.to_csv('flights.csv', index=False)
    
def number_of_csv():
    # Check the number of csv files in our storage
    connection_string = os.environ["BLOB_CONNECTION_STRING"]
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_name = "csv-data"
    container_client = blob_service_client.get_container_client(container_name)
    blob_list = container_client.list_blobs()
    n=0
    for blob in blob_list:
        n+=1
    return str(n)


    
    
def check_for_new_csv():
    # Specify the file path
    file_path = "number.txt"
    
    # Open the file in read mode and read the content
    with open(file_path, 'r') as file:
        last_loaded = file.read().strip()  # Read and strip any extra whitespace
    if last_loaded==number_of_csv():
        return "No new data"
    else:
        return "New data available"


def load_all_data():
    load_data_from_blob()
    st.write('Preparing data for analytics')
    busiest_load()
    covid_load()   
    with open('status.txt', 'w') as file:
        file.write('finished')
    
def busiest_load():
    # Load data
    df = pd.read_csv('flights.csv', usecols=['dep_airport', 'segment'])
    
    # Process data to get total ops per airport
    top_ops = df.groupby('dep_airport').size().reset_index(name='total_ops')

    # Get the top 20 airports by total ops
    top_ops = top_ops.nlargest(20, 'total_ops')['dep_airport']

    # Filter the original dataframe to include only the top airports
    df = df[df['dep_airport'].isin(top_ops)]
    
    # Merge different groups of traditional airlnies in one group   
    traditional_lines =['Traditional Scheduled',
                        'Mainline',
                        'Regional Aircraft']
    df['segment'] = df['segment'].apply(lambda x: 'Traditional Airlines' if x in traditional_lines else x)  

    # Merge smaller categories in 'other'
    values_to_keep= ['All-Cargo',
                     'Not Classified', 
                     'Lowcost', 
                     'Traditional Airlines'
                      ]
    df['segment'] =df['segment'].apply(lambda x: x if x in values_to_keep else 'Other')    
    
    # Calculate ops for each segment within the top airports
    df = df.groupby(['dep_airport', 'segment']).size().reset_index(name='ops')
        
    # Merge with airport information
    airports = pd.read_csv('airport-codes.csv', usecols=['ident', 'name', 'municipality'])
    top_airports = pd.merge(df, airports, left_on='dep_airport', right_on='ident', how='left')

    # Save the result to a CSV file
    top_airports.to_csv('top_airports.csv', index=False)


def covid_load():
    # Load data
    df = pd.read_csv('flights.csv', usecols=['plan_dep', 'segment'])
    
    # Convert 'plan_dep' to datetime format
    df['plan_dep'] = pd.to_datetime(df['plan_dep'], format='%d-%m-%Y %H:%M:%S')

    # Extract year and month into new columns
    df['year'] = df['plan_dep'].dt.year
    df['month'] = df['plan_dep'].dt.month

    # Drop the original 'plan_dep' column
    df = df.drop(columns=['plan_dep'])

    # Merge different groups of traditional airlnies in one group   
    traditional_lines =['Traditional Scheduled',
                        'Mainline',
                        'Regional Aircraft']
    df['segment'] = df['segment'].apply(lambda x: 'Traditional Airlines' if x in traditional_lines else x)  

    #Merge smaller categories in 'Other'
    values_to_keep= ['Not Classified', 
                     'Lowcost', 
                     'Traditional Airlines'
                     ]                      
    df['segment'] = df['segment'].apply(lambda x: x if x in values_to_keep else 'Other') 
    
    # Process data to get total ops per year/month/segment
    total_ops = df.groupby(['year','month','segment']).size().reset_index(name='total_ops')
                  
    # Save the result to a CSV file
    total_ops.to_csv('covid.csv', index=False)
    

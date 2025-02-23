from typing import Any

import pandas as pd
import tabula
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
    #read data about aircraft
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
    flights_delay_data()
    overall_delay_load()
    hourly_delays_load()
    flight_duration_load()
    airports_delays_load()
    # airline_operator_codes_load()
    operators_delays_load()
    plane_dist_load()
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

def flights_delay_data(file_path="flights.csv"):
    if not os.path.exists('delayed_flights_check.csv'):
        try:
            # Load the dataset
            df = pd.read_csv(file_path)
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return
        print(f"Starting file preparation")
        # Convert datetime columns
        datetime_columns = ["plan_dep", "plan_arr", "real_dep", "real_arr"]
        for col in datetime_columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

        # Drop rows where essential datetime values are missing
        df.dropna(subset=["real_dep", "real_arr"], inplace=True)

        # Calculate delay-related features
        df["Flight Duration"] = ((df["real_arr"] - df["real_dep"]).dt.total_seconds() / 60).round()
        df["Departure Delay"] = ((df["real_dep"] - df["plan_dep"]).dt.total_seconds() / 60).round()
        df["Arrival Delay"] = ((df["real_arr"] - df["plan_arr"]).dt.total_seconds() / 60).round()

        # Define delay threshold
        delay_threshold = 15
        df["Delayed"] = (df["Departure Delay"] >= delay_threshold).astype(int)

        # Save the updated dataset
        df.to_csv('delayed_flights_check.csv', index=False)
        print(f"Updated file saved as 'delayed_flights_check.csv' with new columns added.")
        return df
    else:
        print("File 'delayed_flights_check.csv' already exists.")
    return pd.read_csv('delayed_flights_check.csv')

def overall_delay_load(delayed_flights_check="delayed_flights_check.csv"):
    # Load the dataset
    df = pd.read_csv(delayed_flights_check)

    # Group delayed flights
    overall_delay = df.groupby('Delayed').size().reset_index(name='Number of Flights')

    # Save the result to a new CSV file
    overall_delay.to_csv('overall_delay.csv', index=False)
    print(f"Overall delay data saved as 'overall_delay.csv'")
    return overall_delay

def hourly_delays_load(delayed_flights_check="delayed_flights_check.csv"):
    # Load the dataset
    df = pd.read_csv(delayed_flights_check)

    df["real_dep"] = pd.to_datetime(df["real_dep"], errors="coerce")
    # Extract departure time features
    df["Departure Hour"] = df["real_dep"].dt.hour
    bins = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24]
    labels = ['0-2', '2-4', '4-6', '6-8', '8-10', '10-12', '12-14', '14-16', '16-18', '18-20', '20-22', '22-24']
    # Create a new column for the grouped departure hours
    df['Departure Hour Group'] = pd.cut(df['Departure Hour'], bins=bins, labels=labels, right=False)
    df["Departure Hour Group"] = pd.Categorical(df["Departure Hour Group"], ordered=True)
    # Group delayed flights by the new 'Departure Hour Group' column
    hourly_delays = df[df['Delayed'] == 1].groupby('Departure Hour Group').size().reset_index(name='Delayed flights')

    # Save the result to a new CSV file
    hourly_delays.to_csv('hourly_delays.csv', index=False)
    print(f"Hourly delay data saved as 'hourly_delays.csv'")
    return hourly_delays

def flight_duration_load(file_path="delayed_flights_check.csv"):

    df = pd.read_csv(file_path)
    df["Flight Duration Hours"] = df["Flight Duration"] / 60

    bins = [0, 1, 3, 6, 9, 12, float("inf")]
    labels = ["< 1 hour", "1-3 hours", "3-6 hours", "6-9 hours", "9-12 hours", "> 12 hours"]
    #New column for the grouped flight duration
    df["Flight Duration Range"] = pd.cut(df["Flight Duration Hours"], bins=bins, labels=labels, right=False)
    # Filter delayed flights and save the updated dataset
    df_FD = df[df['Delayed'] == 1].groupby('Flight Duration Range').size().reset_index(name='Delayed flights')
    df_FD.to_csv("flight_duration_delay.csv", index=False)
    print(f"Flight duration delays saved as 'flight_duration_delay.csv'")
    return df_FD

def airports_delays_load(file_path="delayed_flights_check.csv"):
    df = pd.read_csv(file_path)
    # Group by departure airport and calculate the proportion of delayed flights
    airport_delays = df.groupby("dep_airport")["Delayed"].mean().reset_index()

    # Load airport codes to get airport names
    airports = pd.read_csv('airport-codes.csv', usecols=['ident', 'name'])
    # Merge airport names into airport_delays dataframe
    airport_delays = airport_delays.merge(airports, left_on='dep_airport', right_on='ident', how='left')
    airport_delays.to_csv("airport_delays.csv", index=False)
    print(f"Airport delays saved as 'airport_delays.csv'")
    return airport_delays

def operators_delays_load(file_path="delayed_flights_check.csv"):
    df = pd.read_csv(file_path)
    # Group by operator and calculate the proportion of delayed flights
    operators_delays = df.groupby("operator")["Delayed"].mean().reset_index()

    operators_delays.to_csv("operators_delays.csv", index=False)
    print(f"Operator delays saved as 'operators_delays.csv'")
    return operators_delays



# def airline_operator_codes_load(file_path="List_of_airline_codes.pdf"):
#
#     # Extract all tables from the PDF
#     tables = tabula.read_pdf("List_of_airline_codes.pdf", pages="all", multiple_tables=True)
#     df = pd.concat(tables)
#     print(df.head())
#     df_filtered = df[["ICAO", "Airline"]]
#
#     # Export to CSV
#     df_filtered.to_csv("airline_codes.csv", index=False)

def plane_dist_load(file_path="flights.csv"):
    #Corelation between aircraft type and distance flown
    # Load the dataset
    df = pd.read_csv(file_path)

    # Filter out rows with missing values in the 'real_distance' column
    df = df.dropna(subset=['real_distance'])

    # Convert the 'real_distance' column to numeric
    df['real_distance'] = pd.to_numeric(df['real_distance'], errors='coerce')

    # Group by aircraft type and calculate the average distance flown
    plane_dist = df.groupby('plane_type')['real_distance'].mean().round().reset_index(name='average_distance')


    # Save the result to a new CSV file
    plane_dist.to_csv('plane_distance.csv', index=False)
    print(f"Average distance flown by aircraft type saved as 'plane_distance.csv'")
    return plane_dist


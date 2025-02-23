
import pandas as pd

def busiest_df(): #df from csv
    df=pd.read_csv('top_airports.csv')
    return df

def covid_df(): #df from csv
    df=pd.read_csv('covid.csv')
    return df

def hourly_delays_df(): #df from csv
    df=pd.read_csv('hourly_delays.csv')
    return df

def delayed_flights_df(): #df from csv
    df=pd.read_csv('delayed_flights_check.csv')#
    return df

def overall_delay_df(): #df from csv
    df=pd.read_csv('overall_delay.csv')
    return df

def flight_duration_delay_df(): #df from csv
    df=pd.read_csv('flight_duration_delay.csv')#
    return df

def airports_delays_df(): #df from csv
    df=pd.read_csv('airport_delays.csv')
    return df

def operators_delays_df(): #df from csv
    df=pd.read_csv('operators_delays.csv')
    return df

def plane_distance_df(): #df from csv
    df=pd.read_csv('plane_distance.csv')
    return df
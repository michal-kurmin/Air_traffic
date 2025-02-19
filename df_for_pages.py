import streamlit as st
import pandas as pd

def busiest_df(): #df from csv
    df=pd.read_csv('top_airports.csv')
    return df

def covid_df(): #df from csv
    df=pd.read_csv('covid.csv')
    return df
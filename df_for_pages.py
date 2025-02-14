import streamlit as st
import pandas as pd

def busiest_df(): #df from csv
    df=pd.read_csv('top_airports.csv')#
    return df



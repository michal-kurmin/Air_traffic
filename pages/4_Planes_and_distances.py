import pandas as pd
import plotly.express as px
import streamlit as st
from df_for_pages import plane_distance_df

# Streamlit title

st.title("Planes & Distances Analysis")

df = plane_distance_df()
# Compare planes and their distances

fig = px.scatter(df, x="average_distance", y="plane_type", color="plane_type", title="Correlation between Planes and Distances Flown")
st.plotly_chart(fig)
st.dataframe(df)
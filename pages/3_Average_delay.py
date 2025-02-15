import streamlit as st
from df_for_pages import average_delay_df
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator
# Load the processed dataset

df = average_delay_df()

# Average Delay by Departure Airport (Top 10 Airports)
top_airports = df["dep_airport"].value_counts().head(10).index
airport_delays = df[df["dep_airport"].isin(top_airports)].groupby("dep_airport")["Delayed"].mean()

st.title("Proportion of Delayed Flights by Top 10 Departure Airports")

fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(airport_delays.index, airport_delays.values, color="red", alpha=0.7)
ax.set_xlabel("Departure Airport")
ax.set_ylabel("Proportion of Delayed Flights")
ax.set_title("Proportion of Delayed Flights by Top 10 Departure Airports")
ax.xaxis.set_major_locator(FixedLocator(range(len(airport_delays.index))))
ax.set_xticklabels(airport_delays.index, rotation=45)
ax.grid(True)

st.pyplot(fig)

st.dataframe(df, use_container_width=True)

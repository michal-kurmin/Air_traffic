import streamlit as st
from df_for_pages import average_delay_df
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator

# Load the processed dataset
df = average_delay_df()

# Streamlit title
st.title("Flights and delays")

# Sidebar checkbox to show/hide the chart
show_chart_byOD = st.sidebar.checkbox("Show Overall distribution of Delay", value=False)
show_chart_byDA = st.sidebar.checkbox("Show Average Delay by Departure Airport (Top 20 Airports)", value=False)
show_chart_byAO = st.sidebar.checkbox("Show Delays by Airline Operator (Top 20 Airports)", value=False)
show_chart_byHD = st.sidebar.checkbox("Show Delay Trend by Hour of the Day", value=False)

if show_chart_byDA:
    # Average Delay by Departure Airport (Top 20 Airports)
    top_airports = df["dep_airport"].value_counts().head(20).index
    airport_delays = df[df["dep_airport"].isin(top_airports)].groupby("dep_airport")["Delayed"].mean()

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(airport_delays.index, airport_delays.values, color="blue", alpha=0.7)
    ax.set_xlabel("Departure Airport")
    ax.set_ylabel("Proportion of Delayed Flights")
    ax.set_title("Proportion of Delayed Flights by Top 20 Departure Airports", pad=10)
    ax.xaxis.set_major_locator(FixedLocator(range(len(airport_delays.index))))
    ax.set_xticklabels(airport_delays.index, rotation=45)
    ax.grid(True)

    st.pyplot(fig)

if show_chart_byAO:
    # Delays by Airline Operator (Top 20 Airlines)
    top_airlines = df["operator"].value_counts().head(20).index
    airline_delays = df[df["operator"].isin(top_airlines)].groupby("operator")["Delayed"].mean()

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(airline_delays.index, airline_delays.values, color="purple", alpha=0.7)
    ax.set_xlabel("Airline Operator")
    ax.set_ylabel("Proportion of Delayed Flights")
    ax.set_title("Proportion of Delayed Flights by Top 20 Airlines", pad=10)
    ax.xaxis.set_major_locator(FixedLocator(range(len(airline_delays.index))))
    ax.set_xticklabels(airline_delays.index, rotation=45)
    ax.grid(True)

    st.pyplot(fig)

if show_chart_byHD:
    # Delay Trend by Hour of the Day
    hourly_delays = df.groupby("Departure Hour")["Delayed"].mean()

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(hourly_delays.index, hourly_delays.values, marker="o", linestyle="-", color="green")
    ax.set_xlabel("Hour of the Day")
    ax.set_ylabel("Proportion of Delayed Flights")
    ax.set_title("Proportion of Delayed Flights by Hour of the Day")
    ax.grid(True)

    st.pyplot(fig)

if show_chart_byOD:
    # Overall distribution of Delay
    fig, ax = plt.subplots(figsize=(12, 6))
    # df["Delayed"].value_counts().plot.pie(autopct='%1.1f%%', ax=ax, colors=['#ff9999','#66b3ff'])
    # ax.set_title("Overall Distribution of Delay", pad=10)

    ax.hist(df["Delayed"], bins=2, color="blue", alpha=0.7, rwidth=0.8)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["On-Time", "Delayed"])
    ax.set_xlabel("Flight Status")
    ax.set_ylabel("Number of Flights")
    ax.set_title("Distribution of Delayed vs. On-Time Flights")
    ax.grid(axis="y")

    st.pyplot(fig)

# Display the dataframe
st.dataframe(df, use_container_width=True)
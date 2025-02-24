import pandas as pd
import plotly.express as px
import streamlit as st
from df_for_pages import hourly_delays_df, overall_delay_df, flight_duration_delay_df, \
    airports_delays_df, operators_delays_df


# Streamlit title

st.title("Delayed flights analysis")
st.write("From the left bar dropdown list, please select the chart to be displayed")

# Sidebar checkbox to show/hide the chart
# Dropdown for selecting one chart at a time
selected_chart = st.sidebar.selectbox(
    "Select a chart to display:",
    [
        "None",
        "Overall Distribution of Delay",
        "Average Delay by Departure Airport (Top 100 Airports)",
        "Delays by Airline Operator (Top 100 Airports)",
        "Delay Trend by Hour of the Day",
        "Impact of Flight Duration on Delay"
    ]
)

# Check which chart was selected
show_chart_None = selected_chart == "None"
show_chart_byOD = selected_chart == "Overall Distribution of Delay"
show_chart_byDA = selected_chart == "Average Delay by Departure Airport (Top 100 Airports)"
show_chart_byAO = selected_chart == "Delays by Airline Operator (Top 100 Airports)"
show_chart_byHD = selected_chart == "Delay Trend by Hour of the Day"
show_chart_byFD = selected_chart == "Impact of Flight Duration on Delay"
st.write(f"Selected Chart: {selected_chart}")

if show_chart_byOD:
    df = overall_delay_df()
    # Overall distribution of Delay
    df["Flight_status"] = df["Delayed"].map({0: "On-Time", 1: "Delayed"})
    fig = px.pie(
        df,
        names="Delayed",
        values="Number of Flights",
        labels={"Delayed": "Flight_status"},
        title="Distribution of Delayed vs. On-Time Flights"
    )

    st.plotly_chart(fig)
    st.dataframe(df)


if show_chart_byDA:
    df = airports_delays_df()
    # Average Delay by Departure Airport
    top_airports = df["name"].value_counts().head(100).index
    airport_delays = df[df["name"].isin(top_airports)].groupby("name")["Delayed"].mean().reset_index()

    fig = px.bar(airport_delays, x="name", y="Delayed",
                 labels={"name": "Departure Airport", "Delayed": "Proportion of Delayed Flights"},
                 title="Delayed Flights by Top 100 Departure Airports")

    st.plotly_chart(fig)
    st.dataframe(df.rename(columns={"name": "Departure airport"})[["Departure airport", "Delayed"]].head(100))


if show_chart_byAO:
    df = operators_delays_df()
    # Delays by Airline Operator (Top 100 Airlines)
    top_airlines = df["operator"].value_counts().head(100).index
    airline_delays = df[df["operator"].isin(top_airlines)].groupby("operator")["Delayed"].mean().reset_index()

    fig = px.bar(airline_delays, x="operator", y="Delayed",
                 labels={"operator": "Airline Operator", "Delayed": "Delayed Flights"},
                 title="Delayed Flights by Top 100 Airlines")

    st.plotly_chart(fig)
    st.dataframe(df[["operator","Delayed"]].head(100))

if show_chart_byHD:
    df = hourly_delays_df()

    # Delay Trend by Hour of the Day
    hourly_delays = df.groupby("Departure Hour Group")["Delayed flights"].mean().reset_index()
    hourly_delays["Departure Hour Group"] = hourly_delays["Departure Hour Group"].astype(str)
    fig = px.line(hourly_delays, x="Departure Hour Group", y="Delayed flights",
                  labels={"Departure Hour Group": "Departure Hour Group", "Delayed flights": "Delayed flights"},
                  title="Delayed Flights by Hour of the Day")

    fig.update_xaxes(type="category")
    st.plotly_chart(fig)
    st.dataframe(df)

if show_chart_byFD:
    df = flight_duration_delay_df()
    # Impact of Flight Duration on Delay
    st.write("Impact of Flight Duration on Delay")

    fig = px.line(df, "Flight Duration Range", "Delayed flights",
                     labels={"Flight Duration Range":"Flight Duration Range", "Delayed flights":"Delayed flights"},
                     title="Impact of Flight Duration on Delay")

    st.plotly_chart(fig)
    st.dataframe(df[["Flight Duration Range", "Delayed flights"]])




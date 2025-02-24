import pandas as pd
import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
from df_for_pages import covid_df

df=covid_df()

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
st.header("Impact of covid on number of montly commercial airtraffic operations")

# Create datetime index
df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=1))
df['sum'] = df.groupby('date')['total_ops'].transform('sum')

# Create the total line chart
fig = px.line(df,
              x='date',
              y='sum',
              title='Monthly total and segmented operations')

# Add individual lines for each segment
for segment in df['segment'].unique():
    segment_data = df[df['segment'] == segment]
    fig.add_scatter(x=segment_data['date'],
                   y=segment_data['total_ops'],
                   name=segment,
                   mode='lines')


# Customize the layout
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Operations",
    legend_title="Segments",
    hovermode='x unified'
)

# Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)

# DataFrames for each season
mon_03 = df[df['month'] == 3]
mon_06 = df[df['month'] == 6]
mon_09 = df[df['month'] == 9]
mon_12 = df[df['month'] == 12]

# Create plots for each group
fig_03 = px.line(mon_03, x='year', y='sum', title='March')
fig_06 = px.line(mon_06, x='year', y='sum', title='June')
fig_09 = px.line(mon_09, x='year', y='sum', title='September')
fig_12 = px.line(mon_12, x='year', y='sum', title='December')

# Create a 2x2 subplot
fig = make_subplots(rows=2, cols=2, subplot_titles=('March', 'June', 'September', 'December'))

# Add the plots to the subplot
fig.add_trace(fig_03['data'][0], row=1, col=1)
fig.add_trace(fig_06['data'][0], row=1, col=2)
fig.add_trace(fig_09['data'][0], row=2, col=1)
fig.add_trace(fig_12['data'][0], row=2, col=2)

# Update layout
fig.update_layout(height=600, width=800,
                  title_text="")
st.header("Sesonal flight impact of covid")
# Display the chart in Streamlit

st.plotly_chart(fig, use_container_width=True)












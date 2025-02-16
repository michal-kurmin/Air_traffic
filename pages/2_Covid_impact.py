import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px

def covid_load():
    # Load data
    df = pd.read_csv('C:/air/flights.csv', usecols=['plan_dep', 'segment'])
    
    print(df.head(3))
    # Convert 'plan_dep' to datetime format
    df['plan_dep'] = pd.to_datetime(df['plan_dep'], format='%d-%m-%Y %H:%M:%S')

    # Extract year and month into new columns
    df['year'] = df['plan_dep'].dt.year
    df['month'] = df['plan_dep'].dt.month

    # Drop the original 'plan_dep' column
    df = df.drop(columns=['plan_dep'])
# =============================================================================
#     
#     # Merge smaller categories in 'other'
#     values_to_keep= ['All-Cargo',
#                      'Not Classified', 
#                      'Lowcost', 
#                      'Traditional Scheduled',
#                      'Charter'                      
#                      ]
# =============================================================================
    
    traditional_lines =['Traditional Scheduled',
                        'Mainline',
                        'Regional Aircraft']


    df['segment'] = df['segment'].apply(lambda x: 'Traditional Airlines' if x in traditional_lines else x)  
    print(df.head(3))
    #Merge smaller categories in 'other'
    values_to_keep= ['Not Classified', 
                     'Lowcost', 
                     'Traditional Airlines'
                     ]                      
    df['segment'] = df['segment'].apply(lambda x: x if x in values_to_keep else 'Other') 
    # Process data to get total ops per year/month/segment
    total_ops = df.groupby(['year','month','segment']).size().reset_index(name='total_ops')
    print(total_ops.head(20))                        
    
        # Save the result to a CSV file
    #top_airports.to_csv('covid.csv', index=False)
    return total_ops


def covid_df(): #df from csv
    df=pd.read_csv('covid.csv')#
    return df

df=covid_load()

# Create a line chart
plt.plot(df['year'], df['total_ops'])

# Adding titles and labels
plt.title('Sample Line Chart')
plt.xlabel('X-axis Label')
plt.ylabel('Y-axis Label')

# Display the chart
plt.show()

# Combine year and month into a single column for the x-axis
df['year_month'] = df['year'].astype(str) + '-' + df['month'].astype(str)

# Pivot the table to get 'year_month' as index and 'segment' as columns
pivot_df = df.pivot(index='year_month', columns='segment', values='total_ops')

# Plotting the line chart
plt.figure(figsize=(10, 6))

# Plot total operations for each segment
for segment in pivot_df.columns:
    plt.plot(pivot_df.index, pivot_df[segment], label=f'Segment {segment}')

# Adding titles and labels
plt.title('Total Operations by Year and Month')
plt.xlabel('Year-Month')
plt.ylabel('Total Operations')
plt.legend()

# Display the chart
plt.show()


# First, let's create a line for total operations
# Assuming your dataframe is called 'df'

# Create datetime index for better x-axis display
df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=1))
df['sum'] = df.groupby('date')['total_ops'].transform('sum')
# Create the total line chart
fig = px.line(df, 
              x='date', 
              y='sum',
              title='Operations by Segment Over Time')

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
    yaxis_title="Total Operations",
    legend_title="Segments",
    hovermode='x unified'
)

# Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)

# Create figure and axis
plt.figure(figsize=(12, 6))

# Create datetime index for better x-axis display
df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=1))

# Plot each segment
for segment in df['segment'].unique():
    segment_data = df[df['segment'] == segment]
    plt.plot(segment_data['date'], segment_data['total_ops'], label=segment)

# Customize the plot
plt.title('Operations by Segment Over Time')
plt.xlabel('Date')
plt.ylabel('Total Operations')
plt.legend()
plt.grid(True)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Display in Streamlit
st.pyplot(plt)
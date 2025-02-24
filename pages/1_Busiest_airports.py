import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from df_for_pages import busiest_df
import numpy as np

df = busiest_df()
    
# Get unique segments
segments = sorted(df['segment'].unique())

# Sidebar controls
st.sidebar.title("Segment Selection")
show_total = st.sidebar.checkbox("Show Total Operations", value=True)

# Create checkboxes for each segment
segment_selections = {}
for segment in segments:
    segment_selections[segment] = st.sidebar.checkbox(f"Show Segment {segment}", value=False)

# Additional options
st.sidebar.title("Display Options")
show_data = st.sidebar.checkbox("Show Data Table", value=True)
show_horizontal = st.sidebar.checkbox("Horizontal chart", value=False)
# Main title
st.markdown("""
<style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 5rem;
        padding-right: 5rem;
    }
    h2 {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)
st.write("")
st.header("Busiest airports by number of monthly commercial operations")

# Slider for number of airports
num_airports = st.slider("Select the number of airports to display", 
                       min_value=3, 
                       max_value=len(df['name'].unique()), 
                       value=5)

# Prepare data for plotting
plot_data = []

# Add total operations if selected
if show_total:
    total_ops = df.groupby('name')['ops'].sum().reset_index()
    total_ops['segment'] = 'Total'
    plot_data.append(total_ops)

# Add selected segment operations
for segment, selected in segment_selections.items():
    if selected:
        segment_ops = df[df['segment'] == segment].groupby('name')['ops'].sum().reset_index()
        segment_ops['segment'] = segment
        plot_data.append(segment_ops)

segment_colors = {
    "All-Cargo": "#FF5733",  
    "Lowcost": "#33FF57",
    "Not Classified": "#3357FF",
    "Other": "#FFD700",
    "Traditional Airlines": "#FF33A6",
    "Total": "#8A2BE2"
}


if not plot_data:
    st.warning("Please select at least one segment or total operations to display.")
else:  
    if show_horizontal == True:

        # Combine all selected data
        plot_df = pd.concat(plot_data)
        
        # Create the plot
        fig, ax = plt.subplots(figsize=(10, 8))  # Changed from (12, 6)
        
        # Get top airports based on total operations
        top_airports = df.groupby('name')['ops'].sum().nlargest(num_airports).index
        plot_df = plot_df[plot_df['name'].isin(top_airports)]
        
        # Create grouped bar chart
        bar_height = 0.8 / len(plot_data)
        
        
        for i, (segment_name, segment_data) in enumerate(plot_df.groupby('segment')):
            y = np.arange(len(top_airports))
            data = [segment_data[segment_data['name'] == airport]['ops'].iloc[0] 
                    if len(segment_data[segment_data['name'] == airport]) > 0 else 0 
                    for airport in top_airports]
            
            bars = ax.barh(y + i * bar_height, data, bar_height, 
                          label=segment_name ,color=segment_colors[segment_name])
            
       
        # Customize the plot for horizontal layout
        ax.set_title('Airport Operations by Segment', pad=20)
        ax.set_ylabel('Airport')  
        ax.set_xlabel('Operations')  
        
        # Adjust tick positions for horizontal bars
        ax.set_yticks(np.arange(len(top_airports)) + bar_height * (len(plot_data)-1)/2)
        ax.set_yticklabels(top_airports, rotation=0, ha='right')  
        
        # Move legend to a better position for horizontal layout
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Adjust layout
        plt.tight_layout()
        
        # Display the plot
        st.pyplot(fig)
    else:
        # Combine all selected data
        plot_df = pd.concat(plot_data)
        
        # Create the plot
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Get top airports based on total operations
        top_airports = df.groupby('name')['ops'].sum().nlargest(num_airports).index
        plot_df = plot_df[plot_df['name'].isin(top_airports)]
        
        # Create grouped bar chart
        bar_width = 0.8 / len(plot_data)
        
        
        for i, (segment_name, segment_data) in enumerate(plot_df.groupby('segment')):
            x = np.arange(len(top_airports))
            data = [segment_data[segment_data['name'] == airport]['ops'].iloc[0] 
                    if len(segment_data[segment_data['name'] == airport]) > 0 else 0 
                    for airport in top_airports]
            
            bars = ax.bar(x + i * bar_width, data, bar_width, 
                         label=segment_name ,color=segment_colors[segment_name])
            
                    
        # Customize the plot
        ax.set_title('Airport Operations by Segment', pad=20)
        ax.set_xlabel('Airport')
        ax.set_ylabel('Operations')
        ax.set_xticks(np.arange(len(top_airports)) + bar_width * (len(plot_data)-1)/2)
        ax.set_xticklabels(top_airports, rotation=45, ha='right')
        
        ax.legend()
        
        # Adjust layout
        plt.tight_layout()
        
        # Display the plot
        st.pyplot(fig)
    
    # Display the data table if selected
    if show_data:
        st.write("### Data Table")
        st.dataframe(plot_df.pivot(index='name', columns='segment', values='ops').reset_index(),hide_index=True)
    
            
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


if not plot_data:
    st.warning("Please select at least one segment or total operations to display.")
else:  
    if show_horizontal == True:

        # Combine all selected data
        plot_df = pd.concat(plot_data)
        
        # Create the plot
        # CHANGE: Adjusted figure size for horizontal layout
        fig, ax = plt.subplots(figsize=(10, 8))  # Changed from (12, 6)
        
        # Get top airports based on total operations
        top_airports = df.groupby('name')['ops'].sum().nlargest(num_airports).index
        plot_df = plot_df[plot_df['name'].isin(top_airports)]
        
        # Create grouped bar chart
        bar_height = 0.8 / len(plot_data)  # CHANGE: bar_width to bar_height
        colors = plt.cm.Set3(np.linspace(0, 1, len(plot_data)))
        
        for i, (segment_name, segment_data) in enumerate(plot_df.groupby('segment')):
            y = np.arange(len(top_airports))  # CHANGE: x to y
            data = [segment_data[segment_data['name'] == airport]['ops'].iloc[0] 
                    if len(segment_data[segment_data['name'] == airport]) > 0 else 0 
                    for airport in top_airports]
            
            # CHANGE: Use barh instead of bar and adjust positions
            bars = ax.barh(y + i * bar_height, data, bar_height,
                          label=segment_name, color=colors[i])
            
            # CHANGE: Adjust value labels for horizontal bars
            for bar in bars:
                width = bar.get_width()  # CHANGE: height to width
                ax.text(width, bar.get_y() + bar.get_height()/2,
                       f'{int(width):,}',
                       ha='left', va='center', rotation=0)
        
        # CHANGE: Customize the plot for horizontal layout
        ax.set_title('Airport Operations by Segment', pad=20)
        ax.set_ylabel('Airport')  # CHANGE: xlabel to ylabel
        ax.set_xlabel('Operations')  # CHANGE: ylabel to xlabel
        
        # CHANGE: Adjust tick positions for horizontal bars
        ax.set_yticks(np.arange(len(top_airports)) + bar_height * (len(plot_data)-1)/2)
        ax.set_yticklabels(top_airports, rotation=0, ha='right')  # CHANGE: xticks to yticks
        
        # CHANGE: Move legend to a better position for horizontal layout
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
        colors = plt.cm.Set3(np.linspace(0, 1, len(plot_data)))
        
        for i, (segment_name, segment_data) in enumerate(plot_df.groupby('segment')):
            x = np.arange(len(top_airports))
            data = [segment_data[segment_data['name'] == airport]['ops'].iloc[0] 
                    if len(segment_data[segment_data['name'] == airport]) > 0 else 0 
                    for airport in top_airports]
            
            bars = ax.bar(x + i * bar_width, data, bar_width, 
                         label=segment_name, color=colors[i])
            
            # Add value labels
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, height,
                       f'{int(height):,}',
                       ha='center', va='bottom', rotation=0)
        
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
        st.dataframe(plot_df.pivot(index='name', columns='segment', values='ops').reset_index())
    
            
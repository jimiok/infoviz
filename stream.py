import pandas as pd
import streamlit as st
import plotly.express as px

# Load your DataFrame from a pickle file
df = pd.read_pickle('data.pkl')

# Ensure the DataFrame has a 'country' column and a 'value' column to visualize
# For this example, we'll assume you have 'Country' and 'Value' columns in your DataFrame

# Create a choropleth map using Plotly
fig = px.choropleth(df, 
                    locations='Region/Country/Area',  # This should be the country name or ISO code
                    locationmode='country names',  # or 'ISO-3' if using 3-letter country codes
                    color='Value',  # The data column you want to visualize
                    hover_name='Region/Country/Area',  # Column to display as hover text
                    color_continuous_scale='Blues',  # Color scale
                    title='Data by Country')

fig.update_geos(showcoastlines=True, coastlinecolor="Black", showland=True, landcolor="lightgray")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


st.plotly_chart(fig, use_container_width=True)
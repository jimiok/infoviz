import pandas as pd
import streamlit as st
import plotly.express as px

# Load your DataFrame from a pickle file
df = pd.read_pickle('excel_pickle.pkl')

# Ensure the DataFrame has a 'country' column and a 'value' column to visualize
# For this example, we'll assume you have 'Country' and 'Value' columns in your DataFrame

st.title("Sustainable Development Goal (SDG) 6: Clean Water and Sanitation")

number = st.slider('Select a year', min_value=2000, max_value=2022, value=2010)

option = st.selectbox(
    "Choose an area:",
    ("URBAN", "RURAL", "ALLAREA"),
)


df = df[(df["Location"] == option) & (df["TimePeriod"] == number)]

# Create a choropleth map using Plotly
fig = px.choropleth(df, 
                    locations='GeoAreaName',  # This should be the country name or ISO code
                    locationmode='country names',  # or 'ISO-3' if using 3-letter country codes
                    color='Value',  # The data column you want to visualize
                    hover_name='GeoAreaName',  # Column to display as hover text
                    color_continuous_scale='Blues',  # Color scale
                    title='Data by Country')

fig.update_geos(
        showcoastlines=True, 
        coastlinecolor="Black", 
        showland=True, 
        landcolor="lightgray",
        center=dict(lat=2, lon=53),  # Set the center of the map (latitude, longitude)
        projection_scale=2.3  # Adjust the zoom level (lower values zoom in more)
    )
fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
fig.update_layout(
    title='Proportion of population using safely managed drinking-water services',
    coloraxis_colorbar=dict(
        title="Access to Clean Drinking Water (%)"  # Custom label
    )
)

#st.plotly_chart(fig, use_container_width=True)

df_mortality = pd.read_pickle('mortality_data.pkl')

df_mortality = df_mortality[(df_mortality["DIM_TIME"] == 2019) & (df_mortality["DIM_SEX"] == "TOTAL")]

# Create a choropleth map using Plotly
fig_2 = px.choropleth(df_mortality, 
                    locations='GEO_NAME_SHORT',  # This should be the country name or ISO code
                    locationmode='country names',  # or 'ISO-3' if using 3-letter country codes
                    color='RATE_PER_100000_N',  # The data column you want to visualize
                    hover_name='GEO_NAME_SHORT',  # Column to display as hover text
                    color_continuous_scale='Blues',  # Color scale
                    title='Data by Country')

fig_2.update_geos(
        showcoastlines=True, 
        coastlinecolor="Black", 
        showland=True, 
        landcolor="lightgray",
        center=dict(lat=2, lon=53),  # Set the center of the map (latitude, longitude)
        projection_scale=2.3  # Adjust the zoom level (lower values zoom in more)
    )
fig_2.update_layout(margin={"r":0,"t":30,"l":0,"b":0})

fig_2.update_layout(
    title='Mortality rate attributed to exposure to unsafe WASH services, 2019',
    coloraxis_colorbar=dict(
        title="Mortality rate per 100 000"  # Custom label
    )
)

df_expectancy = pd.read_pickle('life_expectancy.pkl')
df_expectancy['Year'] = df_expectancy['Year'].astype(int)
df_expectancy['Value'] = df_expectancy['Value'].replace('..', pd.NA)
df_expectancy['Value'] = pd.to_numeric(df_expectancy['Value'], errors='coerce')

df_expectancy = df_expectancy[(df_expectancy["Year"] == number)]


fig_3 = px.choropleth(df_expectancy, 
                    locations='Country Name',  # This should be the country name or ISO code
                    locationmode='country names',  # or 'ISO-3' if using 3-letter country codes
                    color='Value',  # The data column you want to visualize
                    hover_name='Country Name',  # Column to display as hover text
                    color_continuous_scale='Blues',  # Color scale
                    title='Data by Country')

fig_3.update_geos(
        showcoastlines=True, 
        coastlinecolor="Black", 
        showland=True, 
        landcolor="lightgray",
        center=dict(lat=2, lon=53),  # Set the center of the map (latitude, longitude)
        projection_scale=2.3  # Adjust the zoom level (lower values zoom in more)
    )
fig_3.update_layout(margin={"r":0,"t":30,"l":0,"b":0})

fig_3.update_layout(
    title='Life expectancy',
    coloraxis_colorbar=dict(
        title="Life expectancy"  # Custom label
    )
)

if df_expectancy.empty:
    st.write("No data available for the selected year.")

#st.plotly_chart(fig_2, use_container_width=True)
st.plotly_chart(fig, use_container_width=True)
st.plotly_chart(fig_2, use_container_width=True)
st.plotly_chart(fig_3, use_container_width=True)
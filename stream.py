import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from streamlit_autorefresh import st_autorefresh



st.set_page_config(layout="wide", page_icon=":potable_water:")
st.title("Sustainable Development Goal (SDG) 6: Clean Water and Sanitation")
st.caption("Made for CS-E4450 - Explorative Information Visualization D, Aalto University, 2024 by Jimi Oksman")
st.text("This dashboard visualizes data related to SDG 6: Clean Water and Sanitation, focusing on most vulnerable areas, such as Africa and South Asia. "
        "The data is sourced from the United Nations and the World Bank. "
        "Use the sidebar to select the year and the area (urban, rural, or all areas). " 
        "Due to the lack of data for some years and countries, some parts of the dashboard may be empty.")


if 'slider_value' not in st.session_state:
    st.session_state.slider_value = 2010
if 'auto_change' not in st.session_state:
    st.session_state.auto_change = False

# sidebar
st.sidebar.title("Data selection")

st.session_state.auto_change = st.sidebar.checkbox('Automatically change year', value=st.session_state.auto_change)

# Auto-refresh
if st.session_state.auto_change:
    count = st_autorefresh(interval=1000, limit=100, key="fizzbuzzcounter")
    if count % 1 == 0:
        st.session_state.slider_value += 1
        if st.session_state.slider_value > 2022:
            st.session_state.slider_value = 2000


number = st.sidebar.slider('Select a year', min_value=2000, max_value=2022, value=st.session_state.slider_value)

st.session_state.slider_value = number

option = st.sidebar.selectbox(
    "Choose an area:",
    options=["URBAN", "RURAL", "ALLAREA"],
    format_func=lambda x: {"URBAN": "Urban Areas", "RURAL": "Rural Areas", "ALLAREA": "All Areas"}[x]
)

# First map
df = pd.read_pickle('data/excel_pickle.pkl')
df = df[(df["Location"] == option) & (df["TimePeriod"] == number)]

fig = px.choropleth(df, 
                    locations='GeoAreaName',
                    locationmode='country names',
                    color='Value',
                    hover_name='GeoAreaName',
                    hover_data={'Value': ':.2f', "GeoAreaName": False},
                    labels={'Value': 'Access to Clean Drinking Water (%)'},
                    range_color=[0, 100],
                    color_continuous_scale='RdYlGn',
                    )

fig.update_geos(
        showcoastlines=True,
        coastlinecolor="Black",
        showland=True,
        landcolor="lightgray",
        center=dict(lat=2, lon=53),
        projection_scale=2.3
    )

fig.update_layout(
    margin={"r":0,"t":30,"l":0,"b":0}, 
    title='Proportion of population using safely managed drinking-water services',
    coloraxis_colorbar=dict(
        title="Access to Clean Drinking Water (%)"
    ),
    coloraxis_colorbar_title_side="right",
)


# Second map
df_mortality = pd.read_pickle('data/mortality_data.pkl')

df_mortality = df_mortality[(df_mortality["DIM_TIME"] == 2019) & (df_mortality["DIM_SEX"] == "TOTAL")]
df_mortality["log_value"] = np.log10(df_mortality["RATE_PER_100000_N"])


fig_2 = px.choropleth(df_mortality, 
                    locations='GEO_NAME_SHORT',
                    locationmode='country names',
                    color='log_value',
                    hover_name='GEO_NAME_SHORT',
                    hover_data={'RATE_PER_100000_N': ':.2f', "log_value": False, "GEO_NAME_SHORT": False},
                    labels={'RATE_PER_100000_N': 'Mortality rate per 100 000'},
                    color_continuous_scale='RdYlGn_r',
                    title='Data by Country')

fig_2.update_geos(
        showcoastlines=True,
        coastlinecolor="Black",
        showland=True,
        landcolor="lightgray",
        center=dict(lat=2, lon=53),
        projection_scale=2.3
    )

fig_2.update_layout(
    margin={"r":0,"t":30,"l":0,"b":0}, 
    title='Mortality rate attributed to exposure to unsafe WASH services, 2019',
    coloraxis_colorbar=dict(
        title="Mortality rate per 100 000"
    ),
    coloraxis_colorbar_title_side="right",
)

fig_2.update_coloraxes(
    colorbar_tickvals=np.log10([1, 10, 100, 1000, 10000]),
    colorbar_ticktext=["1", "10", "100", "1k", "10k"],
)


# Third map
df_expectancy = pd.read_pickle('data/life_expectancy.pkl')
df_expectancy['Year'] = df_expectancy['Year'].astype(int)
df_expectancy['Value'] = df_expectancy['Value'].replace('..', pd.NA)
df_expectancy['Value'] = pd.to_numeric(df_expectancy['Value'], errors='coerce')

df_expectancy = df_expectancy[(df_expectancy["Year"] == number)]

fig_3 = px.choropleth(df_expectancy, 
                    locations='Country Name',
                    locationmode='country names',
                    color='Value',
                    hover_name='Country Name',
                    hover_data={'Value': ':.2f', "Country Name": False},
                    labels={'Value': 'Life expectancy (years)'},
                    color_continuous_scale='RdYlGn',
                    range_color=[40, 85],
                    title='Data by Country')

fig_3.update_geos(
        showcoastlines=True,
        coastlinecolor="Black",
        showland=True,
        landcolor="lightgray",
        center=dict(lat=2, lon=53),
        projection_scale=2.3
    )

fig_3.update_layout(
    margin={"r":0,"t":30,"l":0,"b":0}, 
    title='Life expectancy',
    coloraxis_colorbar=dict(
        title="Life expectancy (years)"
    ),
    coloraxis_colorbar_title_side="right",
)

if df_expectancy.empty:
    st.write("No data available for the selected year.")


# Fourth map
df_wb_water = pd.read_pickle('data/wb_water_access.pkl')
df_wb_water['Year'] = df_wb_water['Year'].astype(int)
df_wb_water['Value'] = df_wb_water['Value'].replace('..', pd.NA)
df_wb_water['Value'] = pd.to_numeric(df_wb_water['Value'], errors='coerce')

df_wb_water = df_wb_water[(df_wb_water["Area"] == option) & (df_wb_water["Year"] == number)]

fig_4 = px.choropleth(df_wb_water, 
                    locations='Country Name',
                    locationmode='country names',
                    color='Value',
                    hover_name='Country Name',
                    hover_data={'Value': ':.2f', "Country Name": False},
                    labels={'Value': 'Proportion of access (%)'},
                    range_color=[40, 100],
                    color_continuous_scale='RdYlGn',
                    title='Data by Country')

fig_4.update_geos(
        showcoastlines=True,
        coastlinecolor="Black",
        showland=True,
        landcolor="lightgray",
        center=dict(lat=2, lon=53),
        projection_scale=2.3
    )

fig_4.update_layout(
    margin={"r":0,"t":30,"l":0,"b":0}, 
    title='People using at least basic drinking water services',
    coloraxis_colorbar=dict(
        title="Proportion of access (%)"
    ),
    coloraxis_colorbar_title_side="right",
)


# Maps and text
st.plotly_chart(fig, use_container_width=True)
st.text("Access to safely managed drinking-water services is a critical indicator of public health and socio-economic development. "
    "It reflects a country's ability to provide clean, reliable, and sustainable water resources, which are essential for preventing "
    "waterborne diseases and promoting overall well-being. Regions with lower proportions often face higher health risks, economic challenges, "
    "and social inequalities, highlighting areas where targeted interventions and investments are urgently needed.")

st.plotly_chart(fig_4, use_container_width=True)
st.text("Access to basic drinking water services is fundamental to human health and dignity. It serves as a baseline indicator of a community's capacity "
    "to meet essential water needs for drinking, cooking, and hygiene. This map reveals disparities in access, highlighting regions where populations "
    "are vulnerable to waterborne diseases and health crises. Identifying these gaps is crucial for targeting resources and initiatives to improve global "
    "water security and public health.")

st.plotly_chart(fig_2, use_container_width=True)
st.text("This metric highlights the human cost of inadequate water, sanitation, and hygiene (WASH) services. High mortality rates due to unsafe WASH reflect "
    "systemic challenges in access to basic infrastructure and public health services. These deaths are largely preventable, making this data a critical call "
    "to action for investments in clean water, sanitation, and hygiene. Understanding the regional disparities shown on the map helps prioritize efforts to reduce "
    "preventable deaths and promote global health equity.")

st.plotly_chart(fig_3, use_container_width=True)
st.text("Life expectancy is a key indicator of a population's overall health, quality of life, and access to essential services. It reflects the cumulative impact of factors "
    "such as healthcare quality, living conditions, education, and economic stability. Regional disparities in life expectancy highlight areas where improvements in healthcare "
    "systems and social determinants of health are needed.")

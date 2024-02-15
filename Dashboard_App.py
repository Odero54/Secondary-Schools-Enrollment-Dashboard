import streamlit as st # creating an app
import numpy as np
from streamlit_folium import folium_static # using folium on streamlit
import folium # map rendering library
import json # Library to handle json files
from geopy.geocoders import Nominatim # convert an address into longitude and latitude values
import requests # library to handle requests
import pandas as pd # library for data analysis
import plotly.express as px
import plotly.graph_objects as px
import geopandas as gpd # handling geospatial data
import os # navigating file directories
import warnings
import altair as alt
warnings.filterwarnings('ignore')

# Creating header title
st.set_page_config(page_title="Secondary Transitions!!", page_icon=":⏭️:",layout="wide")
st.title("⏭️ 2024 Form One Transitions for Kenyan Counties")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

# Load data
in_file = gpd.read_file(f"{os.getcwd()}//KC_SCH_Enrol.GeoJSON")
csv_data = pd.DataFrame(in_file)
csv_data = csv_data[["County", "% Transition Rate", "% Failed Transition"]]
geo_data = gpd.GeoDataFrame(in_file[["County", "geometry"]])

# Create Maps
def center():
   address = 'Country Kenya'
   geolocator = Nominatim(user_agent="id_explorer")
   location = geolocator.geocode(address)
   latitude = location.latitude
   longitude = location.longitude
   return [latitude, longitude]

# Visualizing our map
#for changing type of the maps
add_select = st.sidebar.selectbox("What basemap do you want to see?",("OpenStreetMap", "Stamen Terrain","Stamen Toner"))
#for calling the function for getting center of maps
centers = center()
#showing the maps
m_kenya = folium.Map(tiles=add_select, location=[centers[0], centers[1]], zoom_start=6)
#design for the app
st.title('Form One Transitions')

# Choropleth Maps
folium.Choropleth(
    geo_data=geo_data,
    name="Form One Transition Rates (%)",
    data=csv_data,
    columns=["County", "% Transition Rate"],
    key_on="feature.properties.County",
    fill_opacity=0.7,
    fill_color="YlGn",
    line_opacity=0.2,
    highlight = True,
    legend_name="Transitions"
).add_to(m_kenya)

cp = folium.Choropleth(
    geo_data=geo_data,
    name="Form One Failed Transition Rates (%)",
    data=csv_data,
    columns=["County", "% Failed Transition"],
    key_on="feature.properties.County",
    fill_opacity=0.7,
    fill_color="Reds",
    line_opacity=0.2,
    highlight = True,
    legend_name="Failed Transitions"
    
).add_to(m_kenya)

# cp.geojson.add_child(folium.features.GeoJsonTooltip
#                                 (fields=['County',in_file],
#                                 aliases=['County: ', in_file],
#                                 labels=True))
folium.LayerControl().add_to(m_kenya)
folium_static(m_kenya)

# st.write(csv_data)
# st.write(alt.Chart(csv_data).mark_bar().encode(
#     x=alt.X('County', sort='ascending'),
#     y='% Transition Rate',
# ))

sorted_csv = csv_data.sort_values(ascending=True, by='% Transition Rate')

fig = px.Figure(data=[px.Bar(
    name = 'Transition Rates',
    x = sorted_csv['County'],
    y = sorted_csv['% Transition Rate']
   ),
                       px.Bar(
    name = '% Failed Transitions',
    x = sorted_csv['County'],
    y = sorted_csv['% Failed Transition'],
    marker_color = 'orange'
   )
])
st.plotly_chart(fig, use_container_width=True)

# fig = px.bar(sorted_csv, x='County', y='% Transition Rate', title='Transition Rate (%)')
# st.plotly_chart(fig, use_container_width=True, color="% Transition Rate")

# fig = px.bar(sorted_csv, x='County', y='% Failed Transition', title='Failed Transition Rate (%)')
# st.plotly_chart(fig, use_container_width=True, color="% Transition Rate")
import folium
from folium import plugins
import pandas as pd
from branca.colormap import LinearColormap
from scraper import *

data = resort_dict
current_temp_list=[]
temperature_colormap = LinearColormap(['blue', 'white', 'red'], vmin=-40, vmax=20)
# Create a map centered around Canada
snowfall_map = folium.Map(location=[56.1304, -106.3468], zoom_start=4)

# Add the MousePosition plugin for hover information
plugins.MousePosition().add_to(snowfall_map)

# Iterate through the data and add CircleMarker for each resort
for key in data.keys():
    resort = data[key]
    latitude = data[key][0]
    longitude=data[key][1]
    snowfall24h=data[key][2]
    snowfall7d=data[key][3]
    snow_base=data[key][4]
    current_temp=data[key][5]
    # Customize radius based on snowfall
    radius = int(snowfall24h) / 2.0

    # Use the colormap to get color based on temperature
    temperature_color = temperature_colormap(int(current_temp))

    # Create a pop-up with information
    popup_text = f"{resort}/n - Snowfall 24H: {snowfall24h} cm /n -  Snowfall 7D: {snowfall7d} cm /n - Snow Base: {snow_base} cm /n- Temperature: {current_temp}°C"

    # Add CircleMarker to the map with a pop-up
    folium.CircleMarker(
        location=[latitude,longitude],
        radius=radius,
        color=temperature_color,  # Set the outline color based on temperature
        fill=True,
        fill_color=temperature_color,  # Set the fill color based on temperature
        fill_opacity=0.7,
        popup=folium.Popup(popup_text, parse_html=True)
    ).add_to(snowfall_map)

# Use colormap for temperature (LinearColormap)


# Add the colormap to the map as a legend
temperature_colormap.caption = 'Temperature (°C)'
temperature_colormap.add_to(snowfall_map)

# Save the map as an HTML file
snowfall_map.save("marmtemperature_and_snowfall_map_with_colormap.html")
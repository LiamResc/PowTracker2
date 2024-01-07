import folium
import math
from folium import plugins
from branca.colormap import LinearColormap
from folium import IFrame
from scraper import *

data = resort_dict

province_input = input('province:')

if province_input == 'All Canada':
    starting_location = [56.1304, -106.3468]
    zoom = 4
elif province_input == 'Alberta':
    starting_location = [52.6279, -118.5916]
    zoom = 6
else:
    starting_location = [51.991422, -120.200058]
    zoom = 6

snowfall_map = folium.Map(location=starting_location, zoom_start=zoom)

# Add the MousePosition plugin for hover information
plugins.MousePosition().add_to(snowfall_map)

radius_input = input('which snowfall to display: ')
# Iterate through the data and add CircleMarker for each resort
for key in data.keys():
    resort = key
    resort_upper = resort.upper()
    latitude = data[key][0]
    longitude = data[key][1]
    snowfall24h = data[key][2]
    snowfall7d = data[key][3]
    snow_base = data[key][4]
    seasonal_snowfall = data[key][5]
    current_temp = data[key][6]

    # Customize radius based on snowfall
    if radius_input == '7 day snowfall':
        radius_size = snowfall7d
    elif radius_input == '24 hour snowfall':
        radius_size = snowfall24h
    elif radius_input == 'Snow base':
        radius_size = snow_base
    else:
        radius_size = seasonal_snowfall
    if radius_size == 'N/A':
        radius_size = 5
    else:
        radius_size = 5 + math.log2(int(radius_size) + 1) * 5

    # Use the colormap to get color based on temperature
    temperature_colormap = LinearColormap(['blue', 'white', 'red'], vmin=-20, vmax=20)
    temperature_color = temperature_colormap(int(current_temp))

    # Create HTML content for pop-up
    popup_html = f"""
    <div style="text-align: center; font-weight: bold;">{resort_upper}</div>
    <div style="text-align: center;">Temperature: {current_temp}°C</div>
    <div style="text-align: center;"> </div>
    <div style="text-align: center;">Base Snow: {snow_base}cm</div>
    <div style="text-align: center;">Snowfall 7 Days: {snowfall7d}cm</div>
    <div style="text-align: center;">Seasonal Snowfall: {seasonal_snowfall}cm</div>
    <div style="text-align: center;">Snowfall 24 Hours: {snowfall24h}cm
    """

    # Create an IFrame to embed the HTML content
    popup_iframe = IFrame(html=popup_html, width=200, height=146)
    popup = folium.Popup(popup_iframe)

    # Add CircleMarker to the map with the pop-up
    folium.CircleMarker(
        location=[latitude, longitude],
        radius=radius_size,
        color=temperature_color,
        fill=True,
        fill_color=temperature_color,
        fill_opacity=0.8,
        popup=popup
    ).add_to(snowfall_map)

# Use colormap for temperature (LinearColormap)
# Add the colormap to the map as a legend
temperature_colormap.caption = 'Temperature (°C)'
temperature_colormap.add_to(snowfall_map)

# Save the map as an HTML file
snowfall_map.save("newtemperature_and_snowfall_map_with_colormap.html")
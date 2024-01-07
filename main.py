import folium
from folium import plugins
import pandas as pd
from branca.colormap import LinearColormap

# Sample data (replace with your own data)
data = pd.DataFrame({
    'Resort': ['Marmott', 'Sunshine', 'Lake Lousie', 'Silver Star', 'Whistler', 'Big White', 'Sun Peaks', 'Revelstoke'],
    'Snowfall': [15, 22, 10, 30, 18, 5, 50, 15],
    'Temperature': [-10, 5, 8, -3, 2, 2, 2, 20],
    'Latitude': [52.8005917, 51.0996056, 51.4249668, 50.35988235473633, 50.1171903, 49.715991, 50.8787669, 50.958621978759766],
    'Longitude': [-118.0833546, -115.772541, -116.177535, -119.0580596923828, -122.9543022, -118.933872, -119.8930944, -118.16400909423828]
})

# Create a map centered around Canada
"""
snow_fall_input = inputs['map_display']


"""
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


snowfall_map = folium.Map(location= starting_location, zoom_start=zoom)

# Add the MousePosition plugin for hover information
plugins.MousePosition().add_to(snowfall_map)


max_temp = max(data['Temperature'], key=abs)
# Use colormap for temperature (LinearColormap)
temperature_colormap = LinearColormap(['blue', 'white', 'red'], vmin = -(max_temp), vmax=(max_temp))

# Iterate through the data and add CircleMarker for each resort
for index, row in data.iterrows():
    snowfall = row['Snowfall']

    # Customize radius based on snowfall
    radius = snowfall / 2.0

    temperature = row['Temperature']

    # Use the colormap to get color based on temperature
    temperature_color = temperature_colormap(temperature)

    # Create a pop-up with information
    popup_text = f"{row['Resort']} - Snowfall: {snowfall} cm, Temperature: {temperature}°C"

    # Add CircleMarker to the map with a pop-up
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=radius,
        color=temperature_color,  # Set the outline color based on temperature
        fill=True,
        fill_color=temperature_color,  # Set the fill color based on temperature
        fill_opacity=0.7,
        popup=folium.Popup(popup_text, parse_html=True)
    ).add_to(snowfall_map)

# Add the colormap to the map as a legend
temperature_colormap.caption = 'Temperature (°C)'
temperature_colormap.add_to(snowfall_map)

# Save the map as an HTML file
snowfall_map.save("temperature_and_snowfall_map_with_colormap.html")
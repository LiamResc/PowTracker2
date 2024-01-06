import folium
from folium import plugins
import pandas as pd

# Sample data (replace with your own data)
data = pd.DataFrame({
    'Resort': ['Marmott', 'Sunshine', 'Lake Lousie', 'Silver Star', 'Whistler','Big White', 'Sun Peaks', 'Revelstoke'],
    'Snowfall': [15, 22, 10, 30, 18, 5, 50, 15],
    'Temperature': [-10, 5, 8, -3, 2, 2, 2, 2],
    'Latitude': [52.8005917, 51.0996056, 51.4249668, 50.35988235473633, 50.1171903,49.715991,50.8787669,50.958621978759766],
    'Longitude': [-118.0833546, -115.772541, -116.177535, -119.0580596923828,-122.9543022,-118.933872,-119.8930944,-118.16400909423828]
})

# Create a map centered around Canada
snowfall_map = folium.Map(location=[56.1304, -106.3468], zoom_start=4)

# Add the MousePosition plugin for hover information
plugins.MousePosition().add_to(snowfall_map)

# Iterate through the data and add CircleMarker for each city
for index, row in data.iterrows():
    snowfall = row['Snowfall']
    
    # Customize color based on snowfall (blue to red gradient)
    color = f"rgb({255 - int(255 * snowfall / data['Snowfall'].max())}, 0, {int(255 * snowfall / data['Snowfall'].max())})"
    
    # Customize radius based on snowfall
    radius = snowfall / 2.0
    
    # Create a pop-up with information
    popup_text = f"{row['Resort']} - Snowfall: {snowfall} cm, Temperature: {row['Temperature']}°C"
    
    # Add CircleMarker to the map with a pop-up
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=radius,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        popup=folium.Popup(popup_text, parse_html=True)
    ).add_to(snowfall_map)

# Save the map as an HTML file
snowfall_map.save("snowfallz_map_with_hover.html")
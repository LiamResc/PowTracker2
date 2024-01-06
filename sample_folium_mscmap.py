import folium

def main(inputs):
    # (1) Folium map
    m = folium_map = folium.Map(location=[53.52826474677026, -113.52982355671745], zoom_start=15, tiles="OpenStreetMap")
    folium.Marker([53.52826474677026, -113.52982355671745], popup="<h1> HackED 2024 Location</h1>", 
    icon=folium.Icon(icon='heart', icon_color='red')).add_to(m)

    folium_map = folium_map._repr_html_()

    return {"folium_map": folium_map, 
            }


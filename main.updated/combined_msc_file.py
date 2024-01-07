import folium
from folium import plugins
import pandas as pd
from branca.colormap import LinearColormap
import requests
from bs4 import BeautifulSoup
import re


def main(inputs):


    resort_dict = {}

    def skimarmot_scraper(resort_dict):

        url = "https://www.skimarmot.com/mountain/weather-conditions/"

        # Send an HTTP request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the element containing the weather information
            weather_group_elements = soup.find_all('div', class_='weather-group')

            for index, weather_group_element in enumerate(weather_group_elements):
                # Check for snow or temperature based on index or other criteria
                if index == 0:
                    snow_info = weather_group_element.text.strip()
                    snow_numbers = re.findall(r'\d+\.\d+|\d+', snow_info)
                    snow_numbers[7] = "N/A"
                    selected_values = [snow_numbers[i] for i in [5, 7, 8, 9]]
                elif index == 1:
                    temperature_info = weather_group_element.text.strip()
                    temperature_numbers = [int(num) for num in re.findall(r'-?\b\d+\b', temperature_info)]            

            
            #values = [latitude, longitude, 24 hour snowfall, 7 day snowfall , Snow base, Seasonal snowfall, Current temperature]
            values = [52.8005917, -118.0833546] + selected_values + [temperature_numbers[1]]

            resort_dict['marmot'] = values

            return resort_dict

        else:
            print(f"Failed to retrieve the page. Status Code: {response.status_code}")

    def weather_revelstoke():
        url = "https://weather.gc.ca/city/pages/bc-65_metric_e.html"

        # Send a GET request to the URL
        response = requests.get(url)

        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")

            # Find the specific element containing the current temperature
            temperature_element = soup.find("p", class_="mrgn-bttm-sm lead mrgn-tp-sm")

            # Extract and print the current temperature
            temperature = temperature_element.text.strip() if temperature_element else "N/A"
            temperature_numeric = re.sub(r'\D', '', temperature)  # Remove non-numeric characters
            return temperature_numeric
        else:
            temp = 0
            return temp
    def revelstoke_scrape(resort_dict):
        # Replace this URL with the actual URL of the website you want to scrape
        url = "https://www.revelstokemountainresort.com/mountain/conditions/snow-report/"

        # Send an HTTP request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Replace these tags and attributes with the actual ones that contain the temperature information
            # Replace these tags and attributes with the actual ones that contain the temperature information
            snow_elements = soup.find_all("span", class_="value")
            # Extract and print the text content of the element
            snow_numbers = []
            for element in snow_elements:
                snow_numbers.append(element.text.strip()) 
            
            # 24 hour snowfall, 7 day snowfall , Snow base, Seasonal snowfall, Current temperature]
            selected_values = [snow_numbers[i] for i in [2, 4, 5, 6]]

            values = [51.0036,-118.2143] + selected_values + [weather_revelstoke()]
            resort_dict['revelstoke'] = values
            return resort_dict

        else:
            resort_dict['revelstoke'] = [51.0036,-118.2143] + [0,0,0,0,0]
            return resort_dict

    def sunpeaks_scrape(resort_dict):
        # Replace this URL with the actual URL of the website you want to scrape
        url = "https://www.sunpeaksresort.com/ski-ride/weather-conditions-cams/weather-snow-report"

        # Send an HTTP request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Replace these tags and attributes with the actual ones that contain the temperature information
            # Replace these tags and attributes with the actual ones that contain the temperature information
            twenfour_hour = soup.find("span", class_="value_switch value_cm snow-24").text.strip()
            seven_hour = soup.find("span", class_="value_switch value_cm snow-7").text.strip()
            snow_base = soup.find("span", class_="value_switch value_cm").text.strip()
            temp = soup.find_all("span", class_="value_switch value_deg")[3].text.strip()
            # Extract and print the text content of the element
            snow_numbers = [twenfour_hour,seven_hour,snow_base,"N/A",temp]

            # 24 hour snowfall, 7 day snowfall , Snow base, Seasonal snowfall, Current temperature]
            values = [50.8820,-119.9056] + snow_numbers
            resort_dict['Sunpeaks'] = values
            return resort_dict

        else:
            resort_dict['Sunpeaks'] = [51.0036,-118.2143] + [0,0,0,0,0]
            return resort_dict


    skimarmot_scraper(resort_dict)
    revelstoke_scrape(resort_dict)
    sunpeaks_scrape(resort_dict)
    print(resort_dict)

    import folium
    import math
    from folium import plugins
    from branca.colormap import LinearColormap


    data = resort_dict




    province_input = inputs['province']

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


    radius_input = inputs['map_display']
    # Iterate through the data and add CircleMarker for each resort
    for key in data.keys():
        resort = key
        resort_upper=resort.upper()
        latitude = data[key][0]
        longitude = data[key][1]
        snowfall24h = data[key][2]
        snowfall7d = data[key][3]
        snow_base = data[key][4]
        seasonal_snowfall = data[key][5]
        current_temp = data[key][6]


        
        # Customize radius based on snowfall
        #radius = int(snowfall24h) 
        
    
        if radius_input == '7 day snowfall':
            radius_size = snowfall7d 
        elif radius_input == '24 hour snowfall':
            radius_size = snowfall24h
        elif radius_input == 'Snow base':
            radius_size = snow_base
        else:
            radius_size = seasonal_snowfall
        if radius_size == 'N/A':
            radius_size=5   
        else:
            radius_size = 5 + math.log2(int(radius_size) + 1) * 5
    


        # Use the colormap to get color based on temperature
        temperature_colormap = LinearColormap(['blue', 'white', 'red'], vmin = -20, vmax=20)
        temperature_color = temperature_colormap(int(current_temp))

        # Create a pop-up with information
        popup_text = f"{resort_upper}\n Current Temperature: {current_temp}°C\n Base Snow: {snow_base}cm\n Snowfall 7 Days: {snowfall7d}cm \n Seasonal Snowfall: {seasonal_snowfall}cm\n Snowfall 24 Hours: {snowfall24h}cm"
        



        # Add CircleMarker to the map with a pop-up
        folium.CircleMarker(
            location=[latitude, longitude],
            radius=radius_size,
            color=temperature_color,  # Set the outline color based on temperature
            fill=True,
            fill_color=temperature_color,  # Set the fill color based on temperature
            fill_opacity=0.8,
            popup=folium.Popup(popup_text, max_width=250, parse_html=True)
        ).add_to(snowfall_map)

    # Use colormap for temperature (LinearColormap)
    # Add the colormap to the map as a legend

    temperature_colormap.caption = 'Temperature (°C)'
    temperature_colormap.add_to(snowfall_map)

    # Save the map as an HTML file
    final_map_html = snowfall_map._repr_html_()
    return {"final_map": final_map_html}
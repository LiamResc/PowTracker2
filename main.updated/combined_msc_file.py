import folium
from folium import plugins
from folium import IFrame
import pandas as pd
import math
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

            resort_dict['Marmot, AB'] = values

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
            resort_dict['Revelstoke, BC'] = values
            return resort_dict

        else:
            resort_dict['Revelstoke, BC'] = [51.0036,-118.2143] + [0,0,0,0,0]
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
            resort_dict['Sunpeaks, BC'] = values
            return resort_dict

        else:
            resort_dict['Sunpeaks, BC'] = [51.0036,-118.2143] + [0,0,0,0,0]
            return resort_dict

    def pano_scraper(resort_dict):
        url = "https://www.panoramaresort.com/panorama-today/daily-snow-report/"

        # Send an HTTP request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the element containing the weather information
            weather_group_elements = soup.find_all('h4', class_='margin-bottom-0')

            snow_numbers = []

            for i in range(8,10):
                original_num = weather_group_elements[i].text.strip()
                new_num = ''.join(char for char in original_num if char.isdigit())
                snow_numbers.append(new_num)
            twentyfour_hour = soup.find_all("h4", class_="margin-bottom-0")[6].text.strip()
            snow_base = soup.find_all("h4", class_="margin-bottom-0")[3].text.strip()
            Twentyfour_hour = ''.join(char for char in twentyfour_hour if char.isdigit())
            Snow_base = ''.join(char for char in snow_base if char.isdigit())
            snow_numbers.append(Twentyfour_hour)
            snow_numbers.append(Snow_base)
            snow_numbers[0],snow_numbers[2] = Twentyfour_hour,snow_numbers[0]
            snow_numbers[1],snow_numbers[2] = snow_numbers[2],snow_numbers[1]


            temp_num = soup.find('div', class_='temp').text.strip()
            Temp_num = '-' if temp_num.startswith('-') else ''
            Temp_num += ''.join(char for char in temp_num if char.isdigit())

            # Check if both snow and temperature information were obtained
            if snow_numbers and Temp_num:
                #values = [latitude, longitude, 24 hour snowfall, 7 day snowfall , Snow base, Seasonal snowfall, Current temperature]
                values = [50.45894339495676, -116.23825137414808] + snow_numbers + [Temp_num]

                resort_dict['Panorama, BC'] = values
                return resort_dict
            else:
                print("Failed to extract snow or temperature information.")

        else:
            print(f"Failed to retrieve the page. Status Code: {response.status_code}")


    def grouse_scrape(resort_dict):
        # Replace this URL with the actual URL of the website you want to scrape
        url = "https://www.grousemountain.com/current_conditions"

        # Send an HTTP request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Replace these tags and attributes with the actual ones that contain the temperature information
            # Replace these tags and attributes with the actual ones that contain the temperature information
            all = soup.find_all("h3", class_="metric")
            twenfour_hour = soup.find_all("h3", class_="metric")[3].text.strip()
            snow_base = soup.find_all("h3", class_="metric")[8].text.strip()
            temp = soup.find_all("h3", class_="metric")[0].text.strip()
            snow_numbers = [twenfour_hour,snow_base,temp]
            for i in range(5,7):
                if i == 5:
                    snow_numbers.insert(1,all[i].text.strip())
                else:
                    snow_numbers.insert(3,all[i].text.strip())
            # Extract and print the text content of the element
            numbers = [int(re.search(r'-?\d+', element).group()) for element in snow_numbers if re.search(r'-?\d+', element)]
            # 24 hour snowfall, 7 day snowfall , Snow base, Seasonal snowfall, Current temperature]
            values = [49.3854,-123.0811] + numbers
            resort_dict['Grouse Mt., B'] = values
            return resort_dict

        else:
            resort_dict['Grouse Mt., BC'] = [49.3854,-123.0811] + [0,0,0,0,0]
            return resort_dict
        
    def bigwhite_scraper(resort_dict):

        url = "https://www.bigwhite.com/mountain-conditions/daily-snow-report"

        # Send an HTTP request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the element containing the weather information
            weather_group_elements = soup.find_all('span', class_='bigger-font')

            snow_numbers = []

            for i in range(4,8):
                original_num = weather_group_elements[i].text.strip()
                new_num = ''.join(char for char in original_num if char.isdigit())
                snow_numbers.append(new_num)




            temp_num = soup.find('span', class_='big-font').text.strip()
            

            # Check if both snow and temperature information were obtained
            if snow_numbers and temp_num:
                #values = [latitude, longitude, 24 hour snowfall, 7 day snowfall , Snow base, Seasonal snowfall, Current temperature]
                values = [49.731427663412234, -118.94392187439394] + snow_numbers + [temp_num]
                resort_dict['Big White, BC'] = values
                return resort_dict
            else:
                print("Failed to extract snow or temperature information.")

        else:
            print(f"Failed to retrieve the page. Status Code: {response.status_code}")


    def lemassif(resort_dict):

        url = "https://www.lemassif.com/en/the-mountain/winter/snow-weather-webcams"

        # Send an HTTP request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the element containing the weather information
            weather_group_elements = soup.find_all('span', class_='metric-value')
            twentfour_hour = weather_group_elements[8].get_text(strip=True).strip("cm")

            snow_numbers = [twentfour_hour]

            for i in range(10,12):
                snow_numbers.append(weather_group_elements[i].get_text(strip=True).strip("cm"))
            snow_numbers.append(weather_group_elements[11].get_text(strip=True).strip("cm"))
            snow_numbers.append(weather_group_elements[0].get_text(strip=True).strip("°C"))

            # Check if both snow and temperature information were obtained
            values = [47.4167, -70.5470] + snow_numbers
            #values = [int(re.search(r'-?\d+(.\d+)?', element).group()) for element in values if re.search(r'-?\d+(.\d+)?', element)]
            resort_dict['Le Massif, QC'] = values
            return resort_dict
            
        else:
            print(f"Failed to retrieve the page. Status Code: {response.status_code}")
    
    lemassif(resort_dict)
    pano_scraper(resort_dict)
    bigwhite_scraper(resort_dict)
    grouse_scrape(resort_dict)
    skimarmot_scraper(resort_dict)
    revelstoke_scrape(resort_dict)
    sunpeaks_scrape(resort_dict)
    data = resort_dict


    province_input = inputs['province']
    radius_input = inputs['map_display']


    if province_input == 'All Canada':
        starting_location = [56.1304, -100.3468]
        zoom = 4
    elif province_input == 'Alberta':
        starting_location = [54.5279, -118.2916]
        zoom = 6
    elif province_input == 'Quebec':
        starting_location = [47, -73]
        zoom = 6
    else:
        starting_location = [50.991422, -120.200058]
        zoom = 6


    snowfall_map = folium.Map(location= starting_location, zoom_start=zoom)
    plugins.MousePosition().add_to(snowfall_map)


    
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
        temperature_colormap = LinearColormap(['blue', 'white', 'red'], vmin = -25, vmax=20)
        temperature_color = temperature_colormap(int(current_temp))

        # Create a pop-up with information
           # Create HTML content for pop-up
        popup_text = f"""
        <div style="text-align: center; font-weight: bold;">{resort_upper}</div>
        <div style="text-align: center;">Temperature: {current_temp}°C</div>
        <div style="text-align: center;"> </div>
        <div style="text-align: center;">Base Snow: {snow_base}cm</div>
        <div style="text-align: center;">Snowfall 7 Days: {snowfall7d}cm</div>
        <div style="text-align: center;">Seasonal Snowfall: {seasonal_snowfall}cm</div>
        <div style="text-align: center;">Snowfall 24 Hours: {snowfall24h}cm
        """

        # Create an IFrame to embed the HTML content
        popup_iframe = IFrame(html=popup_text, width=200, height=146)
        popup = folium.Popup(popup_iframe)



        folium.CircleMarker(
            location=[latitude, longitude],
            radius=radius_size,
            color=temperature_color,  # Set the outline color based on temperature
            fill=True,
            fill_color=temperature_color,  # Set the fill color based on temperature
            fill_opacity=0.8,
            popup=popup
        ).add_to(snowfall_map)

    # Use colormap for temperature (LinearColormap)
    # Add the colormap to the map as a legend

    temperature_colormap.caption = 'Temperature (°C)'
    temperature_colormap.add_to(snowfall_map)

    # Save the map as an HTML file
    final_map_html = snowfall_map._repr_html_()
    return {"final_map": final_map_html}
import requests
from bs4 import BeautifulSoup
import re

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
                snow_numbers = [int(num) for num in re.findall(r'\b\d+\b', snow_info)]
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




print(skimarmot_scraper(resort_dict))
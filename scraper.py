import requests
from bs4 import BeautifulSoup
import re

def skimarmot_scraper():

    url = "https://www.skimarmot.com/mountain/weather-conditions/"

    # Send an HTTP request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the element containing the weather information
        weather_group_elements = soup.find_all('div', class_='weather-group')

        # Initialize dictionaries to store numerical values
        snow_dict = {}
        temperature_dict = {}

        for index, weather_group_element in enumerate(weather_group_elements):
            # Check for snow or temperature based on index or other criteria
            if index == 0:
                snow_info = weather_group_element.text.strip()
                snow_numbers = [int(num) for num in re.findall(r'\b\d+\b', snow_info)]
                selected_values = [snow_numbers[i] for i in [5, 7, 8, 9]]
                snow_labels = ['Last 24 Hours', '2 Days', 'Snow Base', 'Season Total']
                snow_dict = dict(zip(snow_labels, selected_values))
            elif index == 1:
                temperature_info = weather_group_element.text.strip()
                temperature_numbers = [int(num) for num in re.findall(r'-?\b\d+\b', temperature_info)]            
                temperature_labels = ['Mid Mountain 1980m', 'Upper Mountain 2612m']
                temperature_dict = dict(zip(temperature_labels, temperature_numbers[1:]))

        # Print or use the dictionaries as needed
        print(f"Snow Dictionary (cm): {snow_dict}")
        print(f"Temperature Dictionary (°C): {temperature_dict}")

    else:
        print(f"Failed to retrieve the page. Status Code: {response.status_code}")
skimarmot_scraper()
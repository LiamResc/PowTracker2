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
                snow_numbers = re.findall(r'\d+\.\d+|\d+', snow_info)
                snow_numbers[7] = "N/A"
                selected_values = [snow_numbers[i] for i in [5, 7, 8, 9]]
            elif index == 1:
                temperature_info = weather_group_element.text.strip()
                temperature_numbers = [int(num) for num in re.findall(r'-?\b\d+\b', temperature_info)]            

        
        #values = [latitude, longitude, 24 hour snowfall, 7 day snowfall , Snow base, Seasonal snowfall, Current temperature]
        values = [52.8005917, -118.0833546] + selected_values + [temperature_numbers[1]]

        resort_dict['Marmot'] = values

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
        resort_dict['Revelstoke'] = [51.0036,-118.2143] + [0,0,0,0,0]
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

            resort_dict['Big White'] = values
            return resort_dict
        else:
            print("Failed to extract snow or temperature information.")

    else:
        print(f"Failed to retrieve the page. Status Code: {response.status_code}")

bigwhite_scraper(resort_dict)
skimarmot_scraper(resort_dict)
revelstoke_scrape(resort_dict)
sunpeaks_scrape(resort_dict)
print(resort_dict)
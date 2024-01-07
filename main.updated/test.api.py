import requests
from bs4 import BeautifulSoup
import re

# Replace 'YOUR_URL_HERE' with the actual URL of the website
url = 'https://www.bromontmontagne.com/en/detailed-conditions/'

# Make a request to the website and get the HTML content
response = requests.get(url)
html_content = response.content

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all elements with the class 'snowreport-snowfall-box-value-element'
snowfall_element = soup.find(class_='data_metric infos-contitions txt-data-big')
snowfall_element2 = soup.find_all(class_='data_metric infos-contitions txt-data')


# Extract the text from each element and collect the numbers
snowfall_values1 = [element.get_text(strip=True) for element in snowfall_element2]
snowfall_value2= snowfall_element.text.strip()#[element.get_text(strip=True) for element in snowfall_element]

values= list(snowfall_value2.strip(' cm')) + snowfall_values1

values.remove(values[1])


#def BremontTemp(resort_dict):
def weatherGranby():
    url = "https://weather.gc.ca/city/pages/qc-5_metric_e.html"

    # Send a GET request to the URL
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the specific element containing the current temperature
        temperature_element = soup.find("p", class_="mrgn-bttm-sm lead no-obs-icon")

        # Extract and print the current temperature
        temperature = temperature_element.text.strip() if temperature_element else "N/A"
        temperature_numeric = re.search(r'-?\d+(.\d+)?', temperature)
        return int(temperature_numeric.group())
    else:
        temp = 0
        return temp
values.append(weatherGranby())


values[0]=snowfall_value2.strip('cm')
values.insert(3,values[3])
values.remove(values[1])

latitude='45.305'
longitude='-72.637'
values.insert(0,latitude)
values.insert(1,longitude)

my_dict = {'Bromont Mountain, QC': values}
print(my_dict)
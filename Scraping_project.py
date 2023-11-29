#This program scrapes data from Graana.com when location is set to Islamabad

# Importing necessary libraries
from bs4 import BeautifulSoup
import requests
import csv

# List to store the scraped data
data_list = []

# Loop through pages 1 to 3 for example (adjust the range accordingly)
for page_number in range(1, 4):  
   
    try:
        url = f'https://www.graana.com/sale/residential-properties-sale-islamabad-1/?pageSize=30&page={page_number}'
        # Make an HTTP request to the page
        html_text = requests.get(url).text
        

        soup=BeautifulSoup(html_text,'lxml')
        houses=soup.find_all('div',class_='MuiBox-root mui-style-17zbhp0') #Fetch all containers of property listing on a page
        # Loop through each house element
        for house in houses:
            # Extract relevant information from the house element
            Property_type=house.find('div',class_='MuiTypography-root MuiTypography-body2New mui-style-18id7mx').text
            Price=house.find('div',class_='MuiTypography-root MuiTypography-h4New mui-style-gz23my').text
            element_list=[]
            info_elements=house.find_all('div',class_='MuiTypography-root MuiTypography-body2New mui-style-1548769')
            for att in info_elements: #Loop through to get attributes from same class
                element_list.append(att.text.strip())
            Bedrooms=element_list[0]
            Bathrooms=element_list[1]
            Area=element_list[2]

            Location=house.find('h5',class_='MuiTypography-root MuiTypography-subtitle2New mui-style-3bzwbl').text
            # Extract the link and construct the complete URL
            i_link=house.a['href']
            link="https://www.graana.com/" + i_link

            # Create a dictionary for the current house data
            current_data = {
                "Property_type": Property_type,
                "Price": Price,
                "Bedrooms": Bedrooms,
                "Bathrooms": Bathrooms,
                "Area": Area,
                "Location": Location,
                "Link": link
            }
            # Append the current house data to the list    
            data_list.append(current_data)
    except requests.RequestException as e:
        print(f"Error making the request for page {page_number}: {e}")
csv_file_path = 'Propert_data.csv'

fields = ["Property_type", "Price", "Bedrooms", "Bathrooms", "Area", "Location", "Link"]

with open(csv_file_path, 'w', newline='') as csvfile:
    # Creating a CSV writer object
    csvwriter = csv.DictWriter(csvfile, fieldnames=fields)

    # Writing the header
    csvwriter.writeheader()

    # Writing the data
    csvwriter.writerows(data_list)

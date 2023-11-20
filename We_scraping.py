import requests
from bs4 import BeautifulSoup
import csv
import time
import random
def scrape_real_estate_data(location):
    base_url = f'https://www.realtor.com/realestateandhomes-search/{location}'  

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        property_listings = []


        title_selector = '.title'
        price_selector = '.ListPrice'
        url_selector = '.url'

        titles = soup.select(title_selector)
        prices = soup.select(price_selector)
        urls = soup.select(url_selector)

        for title, price, url in zip(titles, prices, urls):
            property_listings.append({
                'Title': title.get_text(strip=True),
                'Price': price.get_text(strip=True),
                'URL': url['href']
            })

        save_to_csv(property_listings)
    else:
        print(f"Failed to retrieve data. Status Code: {response.status_code}")

def save_to_csv(data):
    csv_file = 'real_estate_data.csv'
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['Title', 'Price', 'URL']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f'Data saved to {csv_file}')

if __name__ == "__main__":
    location = 'San-Francisco_CA' 
    scrape_real_estate_data(location)

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from fake_useragent import UserAgent
from time import sleep
from random import randint

ua = UserAgent()

headers = {
  'User-Agent': ua.ie
}

browser = webdriver.Firefox()
browser.get('https://www.leathercountrybags.com/category.cfm')

# Send request to the website
response = requests.get('https://www.leathercountrybags.com/category.cfm?categoriaid_rw=wholesale-handbags&ord=5', headers=headers)

# print(response.text)

# Initialize beautiful soup and parse the response text
soup = BeautifulSoup(response.text, 'html.parser')

products = soup.find_all(class_='btn btn-sm btn-info')

i = 0

items = []

# Loop through each product
for product in products:
  # Get the links for detailed info
  item = product['onclick'].split(',')[2].replace("'", "").replace(";", "")
  items.append(item)

# print(items)

for item in items:

  if i <= 3:
    detail = requests.get('https://www.leathercountrybags.com/' + item, headers=headers)

    soup_dt = BeautifulSoup(detail.text, 'html.parser')

    p = soup_dt.find_all('p')

    print(p)
    
    sleep_time = randint(2, 15) # random numbers for waiting time
    sleep(sleep_time) # pause the loop for some time

    i += 1
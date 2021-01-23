from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from fake_useragent import UserAgent

ua = UserAgent()

headers = {
  'User-Agent': ua.ie
}

# browser = webdriver.Firefox()
# browser.get('https://www.leathercountrybags.com/category.cfm')
# button = browser.find_element_by_css_selector('a.btn.btn-sm.btn-info')

# print(browser)

# Send request to the website
response = requests.get('https://www.leathercountrybags.com/category.cfm?categoriaid_rw=wholesale-handbags&ord=5', headers=headers)

# print(response.text)

# Initialize beautiful soup and parse the response text
soup = BeautifulSoup(response.text, 'html.parser')

products = soup.find_all(class_='btn btn-sm btn-info')

# Loop through each product
for product in products:
  # Get the links for detailed info
  item = product['onclick'].split(',')[2].replace("'", "").replace(";", "")
  print(item)
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from fake_useragent import UserAgent
from time import sleep
from random import randint
from translate import Translator
import lxml

ua = UserAgent()

headers = {
  'User-Agent': ua.ie
}

url = 'https://www.leathercountrybags.com/'

# browser = webdriver.Firefox()
# browser.get('https://www.leathercountrybags.com/category.cfm')

translator = Translator(to_lang='ru')

# Send request to the website
# response = requests.get('https://www.leathercountrybags.com/category.cfm?categoriaid_rw=wholesale-handbags&ord=5', headers=headers)

# print(response.text)

# Initialize beautiful soup and parse the response text
# soup = BeautifulSoup(response.text, 'html.parser')

# products = soup.find_all(class_='btn btn-sm btn-info')

# i = 0

# items = []

# Loop through each product
# for product in products:
  # Get the links for detailed info
  # item = product['onclick'].split(',')[2].replace("'", "").replace(";", "").replace(')', '')
  # items.append(item)
  # print(item)

# print(items)

detail = requests.get(url + 'item.cfm?modale=1&articoloID=10520', headers=headers)

soup_dt = BeautifulSoup(detail.text, 'lxml')

title = translator.translate(soup_dt.find('h3').find('span').get_text())
descs = soup_dt.find(class_='col-md-7').select('p')
description = []
images = soup_dt.select('img.item-thumbnail')
ul = soup_dt.find('ul').select('li')

# Loop through each image and save the files
for image in images:
  image_link = url + image.get('src')
  img_request = requests.get(image_link, 'lxml')

  with open('images/' + image.get('src').split('/')[3], 'wb') as f:
    f.write(img_request.content)

  sleep(randint(2, 7))

print(title)
print(descs)

# Get additional description
for el in ul:
  text = translator.translate(el.text)
  print(text)

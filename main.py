from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from time import sleep
from random import randint
from googletrans import Translator

ua = UserAgent()
translator = Translator()
url = 'https://www.leathercountrybags.com/'

headers = {
  'User-Agent': ua.ie
}

def scrape_data():
  # Send request to the website
  response = requests.get(url + 'category.cfm?categoriaid_rw=wholesale-handbags&ord=5', headers=headers)

  # Initialize beautiful soup and parse the response text
  soup = BeautifulSoup(response.text, 'lxml')

  products = soup.find_all(class_='btn btn-sm btn-info')

  items = []

  # Loop through each product
  for product in products:
    # Get the links for detailed info
    item = product['onclick'].split(',')[2].replace("'", "").replace(";", "").replace(')', '')
    items.append(item)

  for item in items: 

    detail = requests.get(url + item, headers=headers)

    soup_dt = BeautifulSoup(detail.text, 'lxml')

    title = translator.translate(soup_dt.find('h3').find('span').get_text(), dest='ru')
    descs = soup_dt.find(class_='col-md-7').select('p')
    images = soup_dt.select('img.item-thumbnail')
    ul = soup_dt.find('ul').select('li')

    print(title)
    # print(descs)

    # Get additional description
    for el in ul:
      text = translator.translate(el.text, dest='ru')
      print(text)

    # Loop through each image and save the files
    for image in images:
      image_link = url + image.get('src')
      img_request = requests.get(image_link, 'lxml')

      with open('images/' + image.get('src').split('/')[3], 'wb') as f:
        f.write(img_request.content)

      sleep(randint(2, 7))

    sleep(randint(3, 10))

scrape_data()
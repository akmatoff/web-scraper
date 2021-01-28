from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from time import sleep
from random import randint
from googletrans import Translator
from csv import writer

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

    print('Looping through each item...')
    detail = requests.get(url + item, headers=headers)

    soup_dt = BeautifulSoup(detail.text, 'lxml')

    title = translator.translate(soup_dt.find('h3').find('span').get_text(), dest='ru').text
    descs = soup_dt.find(class_='col-md-7').find_all('p')

    description = []
    pics = []
    images = soup_dt.select('img.item-thumbnail')
    ul = soup_dt.find('ul').select('li')

    i = 2

    # Loop through specific range of elements in description
    while i < len(descs) - 4:
      description.append(translator.translate(descs[i].text, dest='ru').text)
      i += 1

    print('Description:', description)

    # Get additional description
    for el in ul:
      text = translator.translate(el.text, dest='ru').text
      description.append(text)

    # Loop through each image and save the files
    for image in images:
      image_link = url + image.get('src')
      img_request = requests.get(image_link, 'lxml')  
      imgname = image.get('src').split('/')[3]
      pics.append('/images/' + imgname)

      with open('images/' + imgname, 'wb') as f:
        f.write(img_request.content)

      print('Saving image...')

      sleep(randint(2, 7))

    sleep(randint(3, 10))

    with open('products.csv', 'a', encoding='utf-8') as csv_file:
      csv_writer = writer(csv_file)
      # Write the received information to a csv file
      csv_writer.writerow([title, '|'.join(description), '|'.join(pics)])
      print('Writing csv file...')

scrape_data()
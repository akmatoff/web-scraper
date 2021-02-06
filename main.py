from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from random import randint
from googletrans import Translator
import csv

ua = UserAgent()
translator = Translator()
url = 'https://www.leathercountrybags.com/'

headers = {
  'User-Agent': ua.ie
}

# Function to write csv file
def write_csv(row):
  with open('products.csv', 'a', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    # Write the received information to a csv file
    csv_writer.writerow(row)
    print('Writing csv file...')

def check_data(data):
  with open('products.csv', newline='') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    if data in reader:
      return True

def scrape_data():

  # Send request to the website
  response = requests.get(url + 'category.cfm?categoriaid_rw=wholesale-handbags&ord=5', headers)

  # Get the page as text
  content = response.text

  # Initialize beautiful soup and parse the response text
  soup = BeautifulSoup(content, 'lxml')

  products = soup.select('div.col-sm-7')
  product_num = 1

  for product in products:
    print('Scraping product number ' + str(product_num))

    title = translator.translate(product.find('span', attrs={'class': None}).text, dest='ru').text
    images = product.select('img.lazy')
    description = translator.translate(product.find_all('p')[2].text, dest='ru').text
    pics = []

    # Loop through each image of a product
    for image in images:
      print('Saving image...')

      img = image['data-original']
      img_link = url + img
      img_request = requests.get(img_link, headers)  
      imgname = img.split('/')[3]
      pics.append(imgname)

      # Save images
      with open('images/' + imgname, 'wb') as f:
        f.write(img_request.content)

    # If row doesn't exist
    if not check_data([title, description, '|'.join(pics)]):
      print('True')
      write_csv([title, description, '|'.join(pics)]) # Call write csv
    
    product_num += 1

scrape_data()
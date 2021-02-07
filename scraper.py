from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from deep_translator import GoogleTranslator
from dotenv import load_dotenv
from instapy import InstaPy
import requests, csv, os

load_dotenv()

ua = UserAgent()
translator = GoogleTranslator(source='auto', target='ru')
url = 'https://www.leathercountrybags.com/'

headers = {
  'User-Agent': ua.ie,
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}

# Function to write csv file
def write_csv(row):
  with open('products.csv', 'a', encoding='utf-8', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    # Write the received information to a csv file
    csv_writer.writerow(row)
    print('Writing csv file...')

# Function to check if data already exists in the csv file
def check_data(data):
  with open('products.csv', encoding='utf-8', newline='') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    data_exists = False

    for row in reader:
      if data in row[0]:
        data_exists = True

  return data_exists
        
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

    product_id = product.find('a').text[0:7].replace('"', '').replace(' ', '').replace('.', '')
    title = translator.translate(product.find('span', attrs={'class': None}).text)
    images = product.select('img.lazy')
    description = translator.translate(product.find_all('p')[2].text)
    pics = []

    print('Product ID', product_id)
    
    exists = check_data(product_id)

    # If row doesn't exist
    if not exists:

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


      write_csv([product_id, title, description, '|'.join(pics)]) # Call write csv
    
    product_num += 1

scrape_data()

def poster():
  instapy = InstaPy(username=os.getenv('USERNAME'), password=os.getenv('PASSWORD'))
from dotenv import load_dotenv
from instabot import Bot
from PIL import Image
import os, shutil, csv

load_dotenv()

username = os.getenv('USERNAMEIG')
password = os.getenv('PASSWORD')

shutil.rmtree('config') if os.path.exists('config') else None

bot = Bot()
bot.login(username=username, password=password)

with open('products.csv', encoding='utf-8', newline='') as csv_file:
    reader = csv.reader(csv_file)

    for row in reader:
        images = row[3].split('|')
        caption = row[2]

        for image in images:
            img = Image.open('images/' + image)
            img.resize((1080, 1080))
            img.save('images/' + image, 'JPEG', quality=100)

            bot.upload_photo('images/' + image)

        with open('posted.csv', 'a', encoding='utf-8', newline='') as csvf:
            writer = csv.writer(csvf)
            writer.writerow([row[0]])
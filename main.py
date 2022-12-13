# Yet another college assignment @Ryukaizen

import click
import os
import pymongo
import random
import requests
import schedule
import smtplib
import time

from datetime import datetime
from dotenv import load_dotenv
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

load_dotenv() 

GMUSER = os.getenv('GMUSER')
GMPASS = os.getenv('GMPASS')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = os.getenv('DB_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

client = pymongo.MongoClient(MONGO_URI, ssl=True)
db = client[f'DB_NAME']
collection = db[f'COLLECTION_NAME']

today = datetime.today()

wishes = ["Count your life by smiles, not tears. Count your age by friends, not years. \n\nHappy birthday! 🥳",
          "Happy birthday! I hope all your birthday wishes and dreams come true. 🎂",
          "May the joy that you have spread in the past come back to you on this day. \n\nWishing you a very happy birthday! 🥳",
          "Wishing you a day filled with happiness and a year filled with joy. \n\nHappy birthday! 🎊🎊🎊",
          "Sending you smiles for every moment of your special day…\n\nHave a wonderful time and a very happy birthday!",
          "May the year ahead be filled with success, happiness, and prosperity. \n\nHappy birthday! 🥳",
          "I hope your birthday is as special as you are. \n\nHappy birthday! 💝",
          "Wishing you a day full of pleasant surprises and a year full of happiness. \n\nHappy birthday! 🎁",
          "May you have a wonderful birthday and a year that is happy and bright. \n\nHappy birthday! 🎉",
          "Happy birthday to you. From good friends and true, from old friends and new, may good luck go with you and happiness too!",    
        ]

images = [ "https://cdn.pixabay.com/photo/2014/06/30/11/40/cupcakes-380178_960_720.jpg",
          "https://cdn.pixabay.com/photo/2016/09/23/03/07/happy-birthday-1688783_960_720.jpg",
          "https://cdn.pixabay.com/photo/2015/05/07/20/35/birthday-cake-757102_960_720.jpg",
          "https://cdn.pixabay.com/photo/2017/08/08/14/39/birthday-2611564_960_720.jpg",
          "https://cdn.pixabay.com/photo/2018/11/24/23/35/gift-3836544_960_720.jpg",
          "https://cdn.pixabay.com/photo/2021/02/10/16/37/wine-6002736_960_720.jpg",
          "https://cdn.pixabay.com/photo/2020/05/13/17/23/strawberry-pie-5168237_960_720.jpg",
          "https://cdn.pixabay.com/photo/2019/07/07/16/09/cake-4322800_960_720.jpg",
        ]

def fetch_birthdays():
    birthdays = []
    query = {"bdday": str(today.day), 
             "bdmonth": str(today.month)}  
    count = collection.count_documents(query)
    if count > 0:
        print("Number of people have their birthday today: ", str(count))
        for doc in collection.find(query):
            print("[*] Today is " + doc['name'] + "'s birthday! " +
                  "They turned " + str(today.year - int(doc['bdyear'])) + " this year.")
            birthdays.append(doc)
        return birthdays
    else:
        print("There are no birthdays today!")
        return False

def generate_ecard(name):
    font = ImageFont.truetype("assets/fonts/GrandHotel-Regular.ttf", 80)
    
    image = random.choice(images)
    response = requests.get(image)
    img = Image.open(BytesIO(response.content))
    draw = ImageDraw.Draw(img)
    text = "Happy Birthday \n" + name + "!"
    draw.text((200, 200), text, font=font, fill=(255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0))
    
    img.save("ecard.jpg")
    return img

def greet_email(name, email):
    msg = MIMEMultipart()
    msg['Subject'] = "Happy Birthday 🎂 " + name + " !!! 🎉🎉🎉"
    msg['From'] = GMUSER
    msg['To'] = email
    
    body = random.choice(wishes)
    
    msg.attach(MIMEText(body, 'plain'))
    msg.attach(MIMEImage(open('ecard.jpg', 'rb').read()))
  
    server = smtplib.SMTP(HOST, PORT)
    server.starttls()
    server.login(GMUSER, GMPASS)
    server.send_message(msg)
    server.quit()
    
    recent_greet = datetime.now().date()
    collection.update_one({'name': name}, {'$set': {'recent_greet': str(recent_greet)}})

def upcoming_birthdays():
    current_day = str(today.day)
    current_month = str(today.month)
    upcoming = collection.find({"bdmonth": current_month})
    for bdays in upcoming:
        if bdays['bdday'] > current_day:
            print("[*] " + bdays['name'] + " has their birthday on " + bdays['bdday'] + "/" + bdays['bdmonth'])
            
def list_birthdays():
    sr_no = 0
    for bdays in collection.find():
        sr_no += 1
        bdaydate = str(bdays['bdday'] + "/" + bdays['bdmonth'] + "/" + bdays['bdyear'])
        form = ("| {} | {} | {} | {} ".format(sr_no, bdays['name'], bdaydate, bdays['email']))
        print(form)
    
def add_birthdays():
    docs = []
    while True: 
        doc = {}
        
        doc['name'] = click.prompt("Enter name")
        doc['email'] = click.prompt("Enter email")
        doc['bdday'] = click.prompt("Enter birthday day")
        doc['bdmonth'] = click.prompt("Enter birthday month")
        doc['bdyear'] = click.prompt("Enter birthday year")
        doc['recent_greet'] = None
        doc['entry_timestamp'] = datetime.utcnow()

        docs.append(doc)
        if click.confirm("""\nEnter "n" to continue adding, "y" if you're done adding""", default=True):
            break
    
    collection.insert_many(docs)
    print("Birthday/s added!")
    
def remove_birthdays():
    while True:
        print("[!] Enter name & email ID of person whose birthday you want to remove")
        name = click.prompt("Enter name")
        email = click.prompt("Enter email")
        try:
            collection.delete_one({'name': name, 'email': email})
        except Exception as e:
            print(e)
            continue
        else:
            print("Birthday/s removed!")
            break
        
def main():
    birthday = fetch_birthdays()
    if birthday != False:
        for person in birthday:
            if person['recent_greet'] == str(datetime.now().date()): # greet only once a day, in case program gets executed multiple times
                print("\n[*] Already greeted " + person['name'] + " today!")
            else:
                generate_ecard(person['name'])
                print("\n[*] Sending greetings on email to " + person['name'] + "...")
                greet_email(person['name'], person['email'])
                print("\nGreeting sent!")
    
    if click.confirm('\nCheck upcoming birthday/s? (Empty output = No upcoming birthdays!)', default=True):
        upcoming_birthdays()
    if click.confirm('\nList all birthday entries?', default=True):
        list_birthdays()
    if click.confirm('\nAdd new birthday/s?', default=True):
        add_birthdays()
    if click.confirm('\nRemove any existing birthday/s?', default=True):
        remove_birthdays()
      
if __name__ == '__main__':
    main()
    print("\nGreeting job is running...\nScheduled to run every day at 00:00 (midnight)...")
    schedule.every().day.at("00:00").do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)      
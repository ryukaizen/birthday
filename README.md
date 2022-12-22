<p align="center" width="100%">
<img src="https://freesvg.org/img/birthday-cake.png" width="100" height="100">
</p>

# Birthday Greeter
Automated birthday greeting script. Made using PyMongo, smtplib and PIL. 

## Features
1. Automated emailing of wishes.
    - Scheduled delivery at 12:00 AM.
    - Random birthday wishes.
    - Current age calculation.
2. Birthday card generation using Pillow.
    - Random birthday card backgrounds.
    - Send as an attachment with emails.
3. MongoDB as database.
    - Add or remove birthdays.
    - Show upcoming birthdays.
    - List every birthday.

## Configuration
Firstly, rename `.env.example` to `.env`.

Configure these environment variables:

`GMUSER = youremail@xyzmail.com`

`GMPASS = password`

`HOST = smtp.gmail.com`

`PORT = 587`

`MONGO_URL = mongodb+srv://<username>:<password>@abcdcluster.mongodb.net/?retryWrites=true&w=majority`

`DB_NAME = your_mongodb_database_name`

`COLLECTION_NAME = your_mongodb_database_collection_name`

Install required modules by doing `pip install -r requirements.txt` in terminal.

To run, simply do `python main.py`.

## To-do
[] Input timeout

[] Custom greetings

[] Print if there are no upcoming birthdays

import datetime as dt
import pandas as pd
import random
import smtplib
from email.message import EmailMessage

# Today date
now = dt.datetime.now()
today_date = (now.month,now.day)

# Birthdays Data
data = pd.read_csv('birthdays.csv')

# Creating a dictionary with useful tuple keys and str values.
birthdays_dates = {
    (row['month'],row['day']):row
    for index, row in data.iterrows()
}

if today_date in birthdays_dates:
    with open(f'letter_templates/letter_{random.randint(1,3)}.txt', 'r') as letter:
        text = letter.read()
        revised = text.replace('[NAME]',birthdays_dates[today_date]['name']).replace('Angela','Soroush Ahmadipanah')

    # Yahoo sender
    my_email = os.environ.get("MY_EMAIL")
    my_password = os.environ.get("MY_PASSWORD")
    receiver_email = birthdays_dates[today_date]['email']

    x = random.randint(1,5)
    with open(f"images/Birthday_img_{x}.jpg", 'rb') as img:
        birthday_img = img.read()

    # email
    email = EmailMessage()
    email['From'] = my_email
    email['To'] = receiver_email
    email['Subject'] = "Happy Birthday"

    email.set_content(revised)

    email.add_attachment(
        birthday_img,
        maintype='image',
        subtype='jpeg',
        filename=f"Birthday_img_{x}.jpg",
    )

    with smtplib.SMTP('smtp.mail.yahoo.com', 587, timeout=30) as connection:
        connection.starttls()
        connection.login(my_email, my_password)
        connection.send_message(email)

    print("Birthday email sent")

else:
    print("Birthday email not sent")

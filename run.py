import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import time
load_dotenv()

def check_school_closure():
    url = 'https://www.wmur.com/weather/closings'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the div for Sanborn Regional School District
    school_div = soup.find('div', class_='weather-closings-data-item', attrs={'data-name': os.getenv("school_name")})

    if school_div:
        status_div = school_div.find('div', class_='weather-closings-data-status')
        if status_div:
            return status_div.text.strip()
    return 'Status not found'

def send_email(status_message):
    sender = 'SCHOOL_ALERT@gmail.com'
    receiver = 'briannippert@gmail.com;rachelnoland20@gmail.com'
    subject = str(os.getenv("school_name")) + ' SNOW DAY!'

    msg = MIMEText(status_message)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    # Replace with your SMTP server details
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(os.getenv("smtp_username"), os.getenv("smtp_password"))
        server.sendmail(sender, receiver, msg.as_string())
        server.close()


def main():
    while True:
        status_message = check_school_closure()
        if status_message and status_message != 'Status not found':
            send_email(status_message)
            print("Email sent with the following status: " + status_message)
        else:
            print("Sanborn Regional School District status not found or school is not closed.")

        # Wait for 1 minute before checking again
        time.sleep(60)

if __name__ == "__main__":
    main()

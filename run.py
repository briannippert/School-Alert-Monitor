import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import time
load_dotenv()

class School():
    def __init__(self, name, sentEmail):
        self.name =name
        self.sentEmail = sentEmail

def check_school_closure(schoolName):
    url = 'https://www.wmur.com/weather/closings'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the div for Given School
    school_div = soup.find('div', class_='weather-closings-data-item', attrs={'data-name': schoolName})

    if school_div:
        status_div = school_div.find('div', class_='weather-closings-data-status')
        if status_div:
            return status_div.text.strip()
    return 'Status not found'

def send_email(status_message, school):
    sender = 'SCHOOL_ALERT@gmail.com'
    subject = school + ' SNOW DAY!'

    msg = MIMEText(status_message)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = os.getenv("email_addresses")
    # Replace with your SMTP server details
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(os.getenv("smtp_username"), os.getenv("smtp_password"))
        server.sendmail(sender, os.getenv("email_addresses"), msg.as_string())
        server.close()


def main():
    schools_str = str.split(os.getenv("school_names"),',')
    schools = []
    for school in schools_str: 
        schools.append(School(school, False))
    while True:
        for school in schools:
            status_message = check_school_closure(school.name)
            if status_message and status_message != 'Status not found':
                if school.sentEmail == False:
                    send_email(status_message, school.name)
                    print("Email sent with the following status: \n" + status_message)
                    school.sentEmail = True
            else:
                print( school.name + ": status not found or school is not closed.")

        # Wait for 1 minute before checking again
        time.sleep(60)

if __name__ == "__main__":
    main()

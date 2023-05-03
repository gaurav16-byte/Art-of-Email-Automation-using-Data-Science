import os
import sys
import sqlite3 as sq
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import csv

def database():
    if os.name == 'nt':
        if 'emaildb.db' not in os.listdir(os.path.expanduser("~") + '\\'):
            conn = sq.connect(os.path.expanduser("~") + '\\emaildb.db')
            cur = conn.cursor()
            cur.execute("CREATE TABLE USERS(email text, name text)")
            cur.execute("INSERT INTO USERS VALUES('t@g.c', 'test')")
            conn.commit()
            conn.close()
        else:
            pass

    elif os.name == 'posix':
        if 'emaildb.db' not in os.listdir(os.path.expanduser("~") + '/Documents/'):
            conn = sq.connect(os.path.expanduser("~") + '/Documents/emaildb.db')
            cur = conn.cursor()
            cur.execute("CREATE TABLE USERS(email text, name text)")
            cur.execute("INSERT INTO USERS VALUES('t@g.c', 'test')")
            conn.commit()
            conn.close()
        else:
            pass

database()

def validate(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def addition():
    if os.name == 'nt':
        conn = sq.connect(os.path.expanduser("~") + '\\emaildb.db')
    elif os.name == 'posix':
        conn = sq.connect(os.path.expanduser("~") + '/Documents/emaildb.db')
    cur = conn.cursor()
        
    with open(os.path.expanduser("~") + '\\report.csv') as file:
        csvreader = csv.reader(file)
        next(csvreader)
        for i in csvreader:
            cur.execute("INSERT INTO USERS VALUES(?, ?)", (i[1], i[2]))
            conn.commit()

    file.close()
    conn.close()
    print("CSV File loaded successfully!")

def send():
    sender_email = "randomfootballer10@gmail.com"
    password = "ihxkiezgbwmozpwi"

    # Create SMTP session
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()

    # Login to the account using the app password
    session.login(sender_email, password)

    if os.name == 'nt':
        conn = sq.connect(os.path.expanduser("~") + '\\emaildb.db')
    elif os.name == 'posix':
        conn = sq.connect(os.path.expanduser("~") + '/Documents/emaildb.db')
    cur = conn.cursor()
    values = []
    for i in cur.execute("SELECT * FROM USERS"):
        values.append([i[0], i[1]])

    for i in values:
        receiver_email = i[0]
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = "EDS Project Test"
        message.attach(MIMEText("Hey! " + i[1], 'plain'))
        # Send email
        text = message.as_string()
        session.sendmail(sender_email, receiver_email, text)
        print("Email sent to", i[0])

    session.quit()
    print('E-Mails Sent Successfully!')

while True:
    print("A)LOAD CSV")
    print("B)SEND EMAIL")
    print("C)EXIT")
    choice = input("> ")
    while choice.lower() not in 'abc':
        print("Invalid Choice")
        choice = input("> ")
    else:
        if choice.lower() == 'a':
            addition()
        elif choice.lower() == 'b':
            send()
        elif choice.lower() == 'c':
            break

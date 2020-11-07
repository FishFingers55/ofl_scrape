from bs4 import BeautifulSoup
import requests
from decimal import Decimal
import os
import smtplib
import time


cheap_desk = 294.99
cheap_table = 124.99
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")

def find(soup):
    p = soup.find("p", class_="main-price")
    return p.span.text

def remove_pound(string):
    return Decimal(string[1:])

def send_mail():
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login("pshearer65@gmail.com", "cjvqakfunlsjaxxl")

    subject = "Oak Furniture Land Prices Dropped"
    body = """Check oak furniture land prices. They have dropped!
    https://www.oakfurnitureland.co.uk/furniture/bevel-natural-solid-oak-computer-desk/1453.html
    https://www.oakfurnitureland.co.uk/furniture/bevel-natural-solid-oak-2-drawer-bedside-table/1440.html"""

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail("pshearer65@gmail.com", "pshearer65@gmail.com", msg)

    server.quit()

while True:
    desk_source = requests.get("https://www.oakfurnitureland.co.uk/furniture/bevel-natural-solid-oak-computer-desk/1453.html").text
    table_source = requests.get("https://www.oakfurnitureland.co.uk/furniture/bevel-natural-solid-oak-2-drawer-bedside-table/1440.html").text

    desk_soup = BeautifulSoup(desk_source, "lxml")
    table_soup = BeautifulSoup(table_source, "lxml")

    desk_price = find(desk_soup)
    table_price = find(table_soup)

    desk_price = remove_pound(desk_price)
    table_price = remove_pound(table_price)

    if desk_price < cheap_desk or table_price < cheap_table:
        send_mail()
    if desk_price < cheap_desk:
        cheap_desk = desk_price
    if table_price < cheap_table:
        cheap_table = table_price

    time.sleep(86400)

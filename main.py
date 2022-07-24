import requests
from bs4 import BeautifulSoup
import time
from PIL import Image,ImageDraw,ImageFont
from waveshare_epd import epd2in13_V2
import sys
import datetime

price_url = "https://www.doviz.com/"  # Website for taking currency info
epd = epd2in13_V2.EPD()  # E-ink screen definition

def dates():
    datestimes = []
    x = datetime.datetime.now()
    x = str(x)
    x = x.split(" ")
    date = x[0].split("-")
    time = x[1].split(".")[0]
    date = date[2] + "." + date[1] + "." + date[0]
    datestimes.append(date)
    datestimes.append(time)

    return datestimes

def full_update_clear():  # Clearing screen
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)


def screen_write(gold, dolar, euro):  # Writing data on the screen
    font24 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18)
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)

    epd.init(epd.FULL_UPDATE)
    epd.displayPartBaseImage(epd.getbuffer(time_image))
    epd.init(epd.PART_UPDATE)

    time_draw.text((17, 10), dates()[0] + "  -", font=font24, fill=0)
    time_draw.text((145, 10), dates()[1], font=font24, fill=0)

    time_draw.text((17, 60), "GOLD", font=font24, fill=0)
    time_draw.text((98, 60), "USD", font=font24, fill=0)
    time_draw.text((166, 60), "EURO", font=font24, fill=0)

    time_draw.text((13, 90), gold, font=font24, fill=0)
    time_draw.text((89, 90), dolar, font=font24, fill=0)
    time_draw.text((165, 90), euro, font=font24, fill=0)
    epd.display(epd.getbuffer(time_image.rotate(180)))


def soup_maker(url):  # Taking source code of the site
    page = requests.get(url)

    if page.status_code == 200:
        soup = BeautifulSoup(page.content, "html.parser")

        return soup



def price_grabber(soup):  # Grabing the price from soup
    doviz = []

    gold = soup.find_all("span", class_="value")[0].get_text()
    dolar = soup.find_all("span", class_="value")[1].get_text()
    euro = soup.find_all("span", class_="value")[2].get_text()

    doviz.append(gold)
    doviz.append(dolar)
    doviz.append(euro)

    return doviz


def main():
    while True:
        screen_write(price_grabber(soup_maker(price_url))[0], price_grabber(soup_maker(price_url))[1], price_grabber(soup_maker(price_url))[2])
        time.sleep(60)

if __name__== '__main__':
    try:
        main()
    except: #if the screen fails to initiate exit
        print("\n")
        print("fail")
        sys.exit(1)

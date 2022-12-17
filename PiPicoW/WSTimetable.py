#biblio do wyswietlacza
import ili9341
#import utime
import mySetup
from machine import Pin, SPI
from sys import implementation
from os import uname
from xglcd_font import XglcdFont

#biblio od rozkladu jazdy
from get_bus import *

#konf od wyswietlacza
led = Pin(21, Pin.OUT)
led.high()
display = mySetup.createMyDisplay()
unispace = XglcdFont('lib/fonts/Unispace12x24.c', 12, 24)
line = "1"
direction = "Potulicka"
departure = "za 12 min"


def print_board(linia, kierunek, odjazd):
    text = "Linia Kierunek      Odjazd"
    
    text2 = '{:' '<3}'.format(linia[:3]) +\
            ' ' + '{:' '<11}'.format(kierunek[:11]) +\
            ' ' + '{:>9}'.format(odjazd[:9])          
    display.draw_text(0, 0, text, unispace,
                      ili9341.color565(10, 200, 252))  # ostatnia wyświetlana linia
    display.draw_text(0, 36, text2, unispace,
                      ili9341.color565(0, 0, 200))
    display.draw_text(0, 72, text2, unispace,
                      ili9341.color565(200, 200, 200))
    display.draw_text(0, 108, text2, unispace,
                      ili9341.color565(200, 200, 200))
    display.draw_text(0, 144, text2, unispace,
                      ili9341.color565(200, 200, 200))
    display.draw_text(0, 180, text2, unispace,
                      ili9341.color565(200, 200, 200))
    display.draw_text(0, 216, text2, unispace,
                      ili9341.color565(200, 20, 10))  # ostatnia wyświetlana linia
    
    
print("lama")    
print_board(line,direction,departure)

# # generowanie przerwań cyklicznych do synchrnizacji czasu z serwerem ntp
# timer = Timer(period=18000000, mode=Timer.PERIODIC, callback=lambda t: ntptime.settime)
#    
# # wczytywanie danych sieci i ur przystanków z pliku konfiguracyjnego   
# with open('config.json', 'r') as f:
#     data = json.load(f)
#     wifi_list = data['networks']
#     stops_list = data['transport_stop']
# 
# 
# while True:
#     while wlan.isconnected() == False:
#         connect_aval_wlan(wifi_list,wlan)   
#         sleep(2)        
#     sleep(3)  # okres odświeżania
#     get_and_display(stops_list) 
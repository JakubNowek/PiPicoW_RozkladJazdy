import urequests as requests
import network
import socket
from time import sleep
from picozero import pico_led
import machine
import re


# ssid = 'UPC7DDE84E'
# password = 'yTu3mP8xedrs'

ssid = 'StrazMiejska47853'
password = '12345678'

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1) 
    print(wlan.ifconfig())
    pico_led.on()
    
    
class pojazd:
    numer = ""
    kierunek = ""
    odjazd = ""
    
tablica = []  
    
    
try:
    connect()
except KeyboardInterrupt:
    machine.reset()
    pico_led.off()
    
res = requests.get(url='https://www.zditm.szczecin.pl/json/tablica.inc.php?lng=pl&slupek=12111&t=0.8450320169628875')
text = res.text
text = r'{"tresc":"<table class=\"tablicagmv\">\r\n\t<thead><tr><th class=\"gmvlinia\">linia<\/th><th class=\"gmvkierunek\">kierunek<\/th><th class=\"gmvgodzina\">odjazd<\/th><\/tr><\/thead>\r\n\t<tbody>\r\n\t\t<tr><td class=\"gmvlinia\">9<\/td><td class=\"gmvkierunek\">Potulicka<\/td><td class=\"gmvgodzina\">za&nbsp;2&nbsp;min<\/td><\/tr>\r\n\t\t<tr><td class=\"gmvlinia\">9<\/td><td class=\"gmvkierunek\">Potulicka<\/td><td class=\"gmvgodzina\">za&nbsp;20&nbsp;min<\/td><\/tr>\r\n\t\t<tr><td class=\"gmvlinia\">9<\/td><td class=\"gmvkierunek\">Potulicka<\/td><td class=\"gmvgodzina\">17:40<\/td><\/tr>\r\n\t\t<tr><td class=\"gmvlinia\">9<\/td><td class=\"gmvkierunek\">Potulicka<\/td><td class=\"gmvgodzina\">17:52<\/td><\/tr>\r\n\t\t<tr><td class=\"gmvlinia\">9<\/td><td class=\"gmvkierunek\">Potulicka<\/td><td class=\"gmvgodzina\">18:04<\/td><\/tr>\r\n\t<\/tbody>\r\n<\/table>","komunikat":""}'
print(text)


flag = 1
while flag == 1:
    m = re.search(r'">(.+?)<\\', text)
    if m:
        flag = 1
        found = m.group(1)
        ind = m.span()[1]
        text = text[ind:]
        print('\n',found,'\n')
        print(ind)
        print(len(found))
        print('\n',text,'\n')
    else:
        flag = 0
        #print(dir(m.group(1)))
print("KAAAAACZKI")

        
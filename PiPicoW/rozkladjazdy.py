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
    
#res = requests.get(url='https://www.zditm.szczecin.pl/json/tablica.inc.php?lng=pl&slupek=12111&t=0.8450320169628875')
res = requests.get(url='https://www.zditm.szczecin.pl/json/tablica.inc.php?lng=pl&slupek=30812&t=0.8865995302992444')
text = res.text
print(text)
text = text.replace('&nbsp;',' ')

flag = 1
while flag == 1:
    m = re.search(r'">(.+?)<\\*', text)
    if m:
        flag = 1
        found = m.group(1)
        ind = m.span()[1]
        text = text[ind:]
        print('\n',found,'\n')
        print('\n',text,'\n')
    else:
        flag = 0
        #print(dir(m.group(1)))
print("------------------------")

# wyswietlanie komunikatu przystanku
print(res.json()['komunikat'])
        
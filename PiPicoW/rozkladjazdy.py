# TODO
# automatyczny wybór WiFi
# zmiana przystanków
# wyświetlanie na wyświetlaczu**
# wyświetlanie polskich znaków***

import urequests as requests
import network
import socket
from time import sleep, ticks_ms as timer
from picozero import pico_led
from machine import reset, Timer
import re
from replaceunicode import txtReplace

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
pico_led.off()
wlan.disconnect()
a = []
def connect(wifi):
    ssid = wifi[0]
    passwd = wifi[1]
    #Connect to WLAN
    wlan.connect(ssid, passwd)
    print("connecting to", ssid)
    sleep(7)
    if wlan.isconnected() == True:    
        print('Connected to:',wlan.ifconfig())
        pico_led.on()
    else:
        print("Connection timed out")
        wlan.disconnect()
      
  
def getAndDisplay():
    
    board = []
    # Plac Galczynskiego (9)   
    #res = requests.get(url='https://www.zditm.szczecin.pl/json/tablica.inc.php?lng=pl&slupek=12111&t=0.8450320169628875')
    # Bogumily (9,1)
    try:
        res = requests.get(url='https://www.zditm.szczecin.pl/json/tablica.inc.php?lng=pl&slupek=30812&t=0.8865995302992444') 
        #res = requests.get(url='https://www.zditm.szczecin.pl/json/tablica.inc.php?lng=pl&slupek=86721&t=0.42515855861867013')
        #print(text)
        text = res.text
        # zamiana znakow HTML i polskich 
        text = txtReplace(text)
        
        match = True
        while match:
            m = re.search(r'">(.+?)<\\*', text)
            if m:
                match = True
                found = m.group(1)
                ind = m.span()[1]
                text = text[ind:]
                board.append(found)
            else:
                match = False
                #print(dir(m.group(1)))
        print(board)        
        print("------------------------")

        # wyswietlanie komunikatu przystanku
        print(res.json()['komunikat'])
        #print('zamienianie czas', end-start)
    except:    
        wlan.disconnect()

connected = False

def interruptHandler():
    if wlan.isconnected() == True:
        print("is connected")
        connected = True
    else:
        print("not connected")
        connected = False
    
# generowanie przerwań cyklicznych do sprawdzania połączenia
timer = Timer(period=10000, mode=Timer.PERIODIC, callback=lambda t: interruptHandler())

# wczytywanie listy wifi jako tupli
with open('config.txt', 'r') as f:
    wifilist = [tuple(i.strip('\n\r').split(',')) for i in f]


while True:
    print('petla')
    
    if wlan.isconnected() == False:
        for n in range (0,3):
            connect(wifilist[n])
            if wlan.isconnected() == True:
                break
    sleep(1)
    




# wifiscan = wlan.scan()
# 
# accessableWifi = []
# for network in wifiscan:
#     for wifi in wifilist:
#         if str(network[0].decode("utf-8")) == wifi[0]:
#             accessableWifi.append(network[0].decode("utf-8"))
# print('znaleziono', accessableWifi)


# n = 0
# 
# while True:
#     print('petla dziala nieskonczona')
#     if n>2:
#         n=0    
#     if wlan.isconnected() == True:
#         getAndDisplay()
#     else:    
#         print('No connection...')
#         connect(wifilist[n])   
#     n+=1
#     sleep(1)

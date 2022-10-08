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
connecting = False


def connect(wifi):
    connecting = True
    ssid = wifi[0]
    passwd = wifi[1]
    #Connect to WLAN
    wlan.connect(ssid, passwd)
    pico_led.off()
    timeout = 20
    time_now = 0
    while wlan.isconnected() == False and time_now < timeout:
        print('Waiting for connection with', ssid)
        sleep(1)
        time_now +=1
    if wlan.isconnected() == True:    
        print('Connected to:',wlan.ifconfig())
        pico_led.on()
    else:
        print("connection timed out")
    connecting = False
      
  
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
        #print('zamienianie czas',end-start)
    except:    
        wlan.disconnect()


def interruptHandler():
    if wlan.isconnected() == False and connecting == False:
        print("Brak połączenia")
        wlan.disconnect()
    else:
        print("connected")     
        
        
        
# generowanie przerwań cyklicznych do sprawdzania połączenia
timer = Timer(period=10000, mode=Timer.PERIODIC, callback=lambda t: interruptHandler())

# wczytywanie listy wifi jako tupli
with open('config.txt', 'r') as f:
    wifilist = [tuple(i.strip('\n\r').split(',')) for i in f]
 


while True:
    if wlan.isconnected() == True:
        getAndDisplay()
    else:    
        print('No connection...')
        print('Retrieving...')
        try:
            connect(wifilist[1])   
        except KeyboardInterrupt:
            machine.reset()
            pico_led.off()
print(dir(wlan))
# print(wlan.scan())
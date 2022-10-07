# TODO
# automatyczny wybór WiFi
# zmiana przystanków
# wyświetlanie na wyświetlaczu
# wyświetlanie polskich znaków

import urequests as requests
import network
import socket
from time import sleep, ticks_ms as timer
from picozero import pico_led
import machine
import re
from replaceunicode import txtReplace

wlan = network.WLAN(network.STA_IF)
wlan.active(True)


def connect(wifi):
    ssid = wifi[0]
    passwd = wifi[1]
    #Connect to WLAN
    wlan.connect(ssid, passwd)
    pico_led.off()
    
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(0.8)
    print('Connected to:',wlan.ifconfig())
    pico_led.on()
  
  
def getAndDisplay():
    
    board = []
    # Plac Galczynskiego (9)   
    #res = requests.get(url='https://www.zditm.szczecin.pl/json/tablica.inc.php?lng=pl&slupek=12111&t=0.8450320169628875')
    # Bogumily (9,1)
    #res = requests.get(url='https://www.zditm.szczecin.pl/json/tablica.inc.php?lng=pl&slupek=30812&t=0.8865995302992444') 
    res = requests.get(url='https://www.zditm.szczecin.pl/json/tablica.inc.php?lng=pl&slupek=86721&t=0.42515855861867013')
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
            #print('\n',found,'\n')
            #print('\n',text,'\n')
            board.append(found)
        else:
            match = False
            #print(dir(m.group(1)))
    print(board)        
    print("------------------------")

    # wyswietlanie komunikatu przystanku
    print(res.json()['komunikat'])
    #print('zamienianie czas',end-start)

# wczytywanie listy wifi jako tupli
with open('config.txt', 'r') as f:
    wifilist = [tuple(i.strip('\n\r').split(',')) for i in f]
 
try:
    connect(wifilist[1])   
except KeyboardInterrupt:
    machine.reset()
    pico_led.off()

while True:
    
    if wlan.isconnected() == False:
        print('Connection lost...')
        print('Retrieving...')
        connect(wifilist[2]) 
    else:    
        getAndDisplay()


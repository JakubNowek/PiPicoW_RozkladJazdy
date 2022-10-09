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


def connect(wifi):
    ssid = wifi[0]
    passwd = wifi[1]
    #Connect to WLAN
    wlan.connect(ssid, passwd)
    print("connecting to", ssid)
    sleep(10)
    if wlan.isconnected() == True:    
        print('Connected to:',wlan.ifconfig())
        pico_led.on()
    else:
        print("Connection timed out")
        wlan.disconnect()
    
    
def accessableWifi(listOfWifi,WLAN):
    wifiscan = WLAN.scan()
    accessList = []
    for network in wifiscan:
        for wifi in listOfWifi:
            if str(network[0].decode("utf-8")) == wifi[0]:
                accessList.append(wifi)
    return accessList


def getAndDisplay():
    
    board = []
    try:
        # Plac Galczynskiego (9)   
        #res = requests.get(url='https://www.zditm.szczecin.pl/json/tablica.inc.php?lng=pl&slupek=12111&t=0.8450320169628875', timeout=15)
        # Bogumily (9,1)
        res = requests.get(url='https://www.zditm.szczecin.pl/json/tablica.inc.php?lng=pl&slupek=30812&t=0.8865995302992444', timeout=15) 
        #res = requests.get(url='https://www.zditm.szczecin.pl/json/tablica.inc.php?lng=pl&slupek=86721&t=0.42515855861867013', timeout=15)
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
        print("HTTP response error")

# connected = False
# def interruptHandler():
#     if wlan.isconnected() == True:
#         print("is connected")
#         connected = True
#     else:
#         print("not connected")
#         connected = False
    
# generowanie przerwań cyklicznych do sprawdzania połączenia
#timer = Timer(period=10000, mode=Timer.PERIODIC, callback=lambda t: interruptHandler())

# wczytywanie listy wifi jako tupli
with open('config.txt', 'r') as f:
    wifilist = [tuple(i.strip('\n\r').split(',')) for i in f]


end = timer()
start = timer()
while True:
    while wlan.isconnected() == False:
        avaliableWifi = accessableWifi(wifilist,wlan)
        start = timer()
        print('Nawiązywanie połączenia')
        if len(avaliableWifi) > 0:
            for n in range (0, len(avaliableWifi)):
                connect(avaliableWifi[n])
                if wlan.isconnected() == True:
                    break
        else:
            print('No wifi avaliable')
            sleep(4)
        sleep(2)    
        end = timer()
        print('Zaktualizowano', (end-start)/1000,'sekund temu.')
    start = timer()
    sleep(3)
    getAndDisplay()
    end = timer()
    print('Zaktualizowano', (end-start)/1000,'sekund temu.') 





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
    print("Connecting to", ssid)
    sleep(10)
    if wlan.isconnected() == True:    
        print('Connected to:',wlan.ifconfig())
        pico_led.on()
    else:
        print("Connection timed out")
        wlan.disconnect()
    
    
def connect_aval_wlan(list_of_wifi,wlan):
    # znajdowanie dostępnych wifi z listy
    wifi_scan = wlan.scan()
    access_list = []
    for network in wifi_scan:
        for wifi in list_of_wifi:
            if str(network[0].decode("utf-8")) == wifi[0]:
                access_list.append(wifi)
    # łączenie ze znalezionymi sieciami              
    print('Nawiązywanie połączenia')
    if len(access_list) > 0:
        for n in range (0, len(access_list)):
            connect(access_list[n])
            if wlan.isconnected() == True:
                break
    else:
        print('No wifi avaliable')
        sleep(4)             


def get_and_display():
    
    board = []
    try:
        # Plac Galczynskiego (9)   
        #res = requests.get(url='https://www.zditm.szczecin.pl/json/tablica.inc.php?lng=pl&slupek=12111&t=0.8450320169628875', timeout=15)
        # Bogumily (9,1)
        res = requests.get(url='https://www.zditm.szczecin.pl/json/tablica.inc.php?lng=pl&slupek=30812&t=0.8865995302992444', timeout=15) 
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
# def interrupt_handler():
#     if wlan.isconnected() == True:
#         print("is connected")
#         connected = True
#     else:
#         print("not connected")
#         connected = False
    
# generowanie przerwań cyklicznych do sprawdzania połączenia
#timer = Timer(period=10000, mode=Timer.PERIODIC, callback=lambda t: interrupt_handler())

# wczytywanie listy wifi jako tupli
with open('config.txt', 'r') as f:
    wifi_list = [tuple(i.strip('\n\r').split(',')) for i in f]


end = timer()
start = timer()

while True:
    
    while wlan.isconnected() == False:
        start = timer()
        connect_aval_wlan(wifi_list,wlan)   
        sleep(2)    
        end = timer()
        print('Zaktualizowano', (end-start)/1000,'sekund temu.')
        
    start = timer()
    sleep(3)
    get_and_display()
    end = timer()
    print('Zaktualizowano', (end-start)/1000,'sekund temu.') 





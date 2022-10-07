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
  
  
def txtReplacePL(txt):
    txt = txt.replace('&nbsp;',' ')
    txt = txt.replace('<blink>&gt;&gt;&gt;','TERAZ')
    txt = txt.replace(r'\u0105','ą')
    #txt = txt.replace(r'\u0104','Ą')
    txt = txt.replace(r'\u0107','ć')
    #txt = txt.replace(r'\u0106','Ć')
    txt = txt.replace(r'\u0119','ę')
    #txt = txt.replace(r'\u0118','Ę')
    txt = txt.replace(r'\u0142','ł')
    txt = txt.replace(r'\u0141','Ł')
    txt = txt.replace(r'\u0144','ń')
    #txt = txt.replace(r'\u0143','Ń')
    txt = txt.replace(r'\u00f3','ó')
    #txt = txt.replace(r'\u00d3','Ó')
    txt = txt.replace(r'\u015b','ś')
    txt = txt.replace(r'\u015a','Ś')
    txt = txt.replace(r'\u0179','ź')
    txt = txt.replace(r'\u017a','Ź')
    txt = txt.replace(r'\u017c','ż')
    txt = txt.replace(r'\u017b','Ż')
    return txt

def txtReplace(txt):
    txt = txt.replace('&nbsp;',' ')
    txt = txt.replace('<blink>&gt;&gt;&gt;','TERAZ')
    txt = txt.replace(r'\u0105','a')
    #txt = txt.replace(r'\u0104','A')
    txt = txt.replace(r'\u0107','c')
    #txt = txt.replace(r'\u0106','C')
    txt = txt.replace(r'\u0119','e')
    #txt = txt.replace(r'\u0118','E')
    txt = txt.replace(r'\u0142','l')
    txt = txt.replace(r'\u0141','L')
    txt = txt.replace(r'\u0144','n')
    #txt = txt.replace(r'\u0143','N')
    txt = txt.replace(r'\u00f3','o')
    #txt = txt.replace(r'\u00d3','O')
    txt = txt.replace(r'\u015b','s')
    txt = txt.replace(r'\u015a','S')
    txt = txt.replace(r'\u0179','z')
    txt = txt.replace(r'\u017a','Z')
    txt = txt.replace(r'\u017c','z')
    txt = txt.replace(r'\u017b','Z')
    return txt


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


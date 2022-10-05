import urequests as requests
import network
import socket
from time import sleep, ticks_ms as timer
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
   
# Plac Galczynskiego (9)   
#res = requests.get(url='https://www.zditm.szczecin.pl/json/tablica.inc.php?lng=pl&slupek=12111&t=0.8450320169628875')
# Bogumily (9,1)
#res = requests.get(url='https://www.zditm.szczecin.pl/json/tablica.inc.php?lng=pl&slupek=30812&t=0.8865995302992444')
res = requests.get(url='https://www.zditm.szczecin.pl/json/tablica.inc.php?lng=pl&slupek=86721&t=0.42515855861867013')
text = res.text
print(text)

# zamiana znakow HTML i polskich 
#start = timer()
text = text.replace('&nbsp;',' ')
text = text.replace('<blink>&gt;&gt;&gt;','TERAZ')
text = text.replace(r'\u0105','ą')
#text = text.replace(r'\u0104','Ą')
text = text.replace(r'\u0107','ć')
#text = text.replace(r'\u0106','Ć')
text = text.replace(r'\u0119','ę')
#text = text.replace(r'\u0118','Ę')
text = text.replace(r'\u0142','ł')
text = text.replace(r'\u0141','Ł')
text = text.replace(r'\u0144','ń')
#text = text.replace(r'\u0143','Ń')
text = text.replace(r'\u00f3','ó')
#text = text.replace(r'\u00d3','Ó')
text = text.replace(r'\u015b','ś')
text = text.replace(r'\u015a','Ś')
text = text.replace(r'\u0179','ź')
text = text.replace(r'\u017a','Ź')
text = text.replace(r'\u017c','ż')
text = text.replace(r'\u017b','Ż')
#end = timer()

flag = 1
while flag == 1:
    m = re.search(r'">(.+?)<\\*', text)
    if m:
        flag = 1
        found = m.group(1)
        ind = m.span()[1]
        text = text[ind:]
        print('\n',found,'\n')
        #print('\n',text,'\n')
    else:
        flag = 0
        #print(dir(m.group(1)))
print("------------------------")

# wyswietlanie komunikatu przystanku
print(res.json()['komunikat'])

#print('zamienianie czas',end-start)

# s = "abc&def#ghi"
# print(s.translate(str.maketrans({'&': '\&', '#': '\#'}))
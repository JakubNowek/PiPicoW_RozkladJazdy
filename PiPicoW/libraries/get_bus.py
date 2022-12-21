from re import search
import urequests as requests
from network import WLAN, STA_IF
#import socket
from ntptime import host as ntphost 
from time import sleep, localtime, ticks_ms
#from picozero import pico_led
from machine import reset, Timer
from replaceunicode import txtReplace
import json

# Preparing WLAN
wlan = WLAN(STA_IF)
wlan.active(True)
wlan.disconnect()
ntphost = "tempus1.gum.gov.pl"


def connect(wifi):
    ssid = wifi[0]
    passwd = wifi[1]
    #Connect to WLAN
    wlan.connect(ssid, passwd)
    print("Connecting to", ssid)
    sleep(10)
    if wlan.isconnected() == True:    
        print('Connected to:',wlan.ifconfig())
        #pico_led.on()
    else:
        print("Connection timed out")
        wlan.disconnect()
        #pico_led.off()
    
    
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

def last_update_t():
    last_update = localtime()
    return f'{last_update[3]}:{last_update[4]:02d}:{last_update[5]:02d}'


def get_and_display(board_list, stp_ID):
    """
    Funkcja pobiera dane z linku url zawartego w board_list, przeksztalca je i zwraca w formie slownka
    @param: board_list - slownik zawierajacy nazwe przystanku oraz adres url do jego danych
    
    @return slownik zawierajacy przetworzone (human readable) dane o przystanku 
    """
    board = []
    bus_stop = {"Name": None, "Departures":[], "Message": None, "Update": None}
    try:
        # Bogumily (9,1) - board_list[1][1]
        page = requests.get(url=board_list[stp_ID][1], timeout=15).json()
    except:
        print("HTTP response error")
    else:    
        text = page["tresc"]
        komunikat = page["komunikat"]
        
        # zamiana znakow HTML i polskich 
        text = txtReplace(text)
        bus_stop["Message"] = txtReplace(komunikat)\
                              
        bus_stop["Name"] = board_list[stp_ID][0]
        # ekstrakcja potrzebnych danych z pliku html
        match = True
        while match:
            m = search(r'">(.+?)<\\*', text)
            if m:
                match = True
                found = m.group(1)
                ind = m.span()[1]
                text = text[ind:]
                board.append(found)
            else:
                match = False
                #print(dir(m.group(1)))        
        bus_stop["Departures"] = board[4:]
        bus_stop["Update"] = last_update_t()
        return bus_stop
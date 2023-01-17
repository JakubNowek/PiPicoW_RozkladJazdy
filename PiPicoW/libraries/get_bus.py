from re import search
import urequests as requests
from network import WLAN, STA_IF
#import socket
from ntptime import host as ntphost 
from time import sleep, localtime, ticks_ms, gmtime
from machine import reset, Timer, RTC
from replaceunicode import txtReplace
import json

import socket
import struct

# Preparing WLAN
wlan = WLAN(STA_IF)
wlan.active(True)
wlan.disconnect()

NTP_DELTA = 2208988800-3600  # -3600 for adjusting to local (Polish) timezone
host = "tempus1.gum.gov.pl"
#host = "pool.ntp.org"

# https://gist.github.com/aallan/581ecf4dc92cd53e3a415b7c33a1147c


def set_time():
    """
    Function synchronises local time with NTP server.
    Created by https://gist.github.com/aallan/581ecf4dc92cd53e3a415b7c33a1147c
    """
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(1)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
    finally:
        s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    t = val - NTP_DELTA    
    tm = gmtime(t)
    RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))


def connect(wifi):
    """
    Function responsible for connecting to given wifi network.
    @param: wifi - list containing wifi credentials
    @param: wlan - WLAN object
    
    """
    ssid = wifi[0]
    passwd = wifi[1]
    #Connect to WLAN
    wlan.connect(ssid, passwd)
    print("Connecting to", ssid)
    sleep(10)
    if wlan.isconnected() == True:    
        print('Connected to:', wlan.ifconfig())
    else:
        print("Connection timed out")
        wlan.disconnect()
    
    
def connect_aval_wlan(list_of_wifi,wlan):
    """
    Function responsible for finding avaliable wifis from the given list and connecting
    to one of them.
    @param: list_of_wifi
    @param: wlan - WLAN object
    
    """
    # finding avaliable wifi from list
    wifi_scan = wlan.scan()
    access_list = []
    for network in wifi_scan:
        for wifi in list_of_wifi:
            if str(network[0].decode("utf-8")) == wifi[0]:
                access_list.append(wifi)
    # connecting to found wifi             
    print('Nawiązywanie połączenia')
    if len(access_list) > 0:
        for n in range (0, len(access_list)):
            connect(access_list[n])
            if wlan.isconnected() == True:
                break           
    else:
        print('No wifi avaliable')
        sleep(4)
    # if connected, synchronise RTC with NTP server    
    try:
        set_time()
    except:
        error_msg("BLAD POBIERANIA CZASU",last_update_t())
        sleep(1)     


def last_update_t():
    """
    Function provides current time in for of an fstring (h:mm:ss)
    
    """
    last_update = localtime()
    return f'{last_update[3]}:{last_update[4]:02d}:{last_update[5]:02d}'


def get_and_display(board_list, stp_ID):
    """
    Function aquires data from url address included in board_list, and transforms it into
    dictionary containing information about chosen bus stop
    @param: board_list - list containing names of bus stops, urls and public transport lines' numbers;
    @param: stp_ID - ID of a given stop;
    @return dictionary containing human readable data of a bus stop specified by stp_ID
    
    """
    board = []
    bus_stop = {"Name": None, "Departures":[], "Message": None, "Update": None}
    try:
        page = requests.get(url=board_list[stp_ID][1], timeout=15).json()
    except:
        print("HTTP response error")
    else:    
        text = page["tresc"]
        komunikat = page["komunikat"]
        
        # replacing html signs and Polish letters
        text = txtReplace(text)
        bus_stop["Message"] = txtReplace(komunikat)               
        bus_stop["Name"] = board_list[stp_ID][0]
        
        # extracting needed data from html file
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
        bus_stop["Departures"] = board[4:]
        bus_stop["Update"] = last_update_t()
        return bus_stop
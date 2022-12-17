# TODO
# zmiana przystanków

from get_bus import *
from get_display import *
    
def chunks(lst, step):
    for i in range(0, len(lst), step):
        yield tuple(lst[i:i + step])
        
        
# generowanie przerwań cyklicznych do synchrnizacji czasu z serwerem ntp
timer = Timer(period=18000000, mode=Timer.PERIODIC, callback=lambda t: ntptime.settime)
   
# wczytywanie danych sieci i url przystanków z pliku konfiguracyjnego   
with open('config.json', 'r') as f:
    data = json.load(f)
    wifi_list = data['networks']
    stops_list = data['transport_stop']

while True:
    while wlan.isconnected() == False:
        connect_aval_wlan(wifi_list,wlan)   
        sleep(2)        
    sleep(3)  # okres odświeżania
    bus_stop = get_and_display(stops_list) # pobieranie danych z przystanku
    
    departures = bus_stop["Departures"]
    # zamiana listy na listę tupli 3-elementowych
    dep = list(chunks(departures,3))[:5]
    print_board(dep,bus_stop["Update"],bus_stop["Name"]) 
    

# TODO
# zmiana przystanków
# wyświetlanie na wyświetlaczu**
# wyświetlanie polskich znaków****

from get_bus import *
from get_display import *
    
# generowanie przerwań cyklicznych do synchrnizacji czasu z serwerem ntp
timer = Timer(period=18000000, mode=Timer.PERIODIC, callback=lambda t: ntptime.settime)
   
# wczytywanie danych sieci i ur przystanków z pliku konfiguracyjnego   
with open('config.json', 'r') as f:
    data = json.load(f)
    wifi_list = data['networks']
    stops_list = data['transport_stop']


while True:
    while wlan.isconnected() == False:
        connect_aval_wlan(wifi_list,wlan)   
        sleep(2)        
    sleep(3)  # okres odświeżania
    get_and_display(stops_list)
    print_board("1","Dupsko","za 69 min") 
    

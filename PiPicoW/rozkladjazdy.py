# TODO
# zmiana przystanków

from get_bus import *
from get_display import *


# defining input button pins for shifting stops
prev_btn = 2
next_btn = 3
# setting up the pins for shifting
ch_prev = Pin(prev_btn,Pin.IN, Pin.PULL_UP)
ch_next = Pin(next_btn,Pin.IN, Pin.PULL_UP)


def prev_btn_handler(pin):
    global stop_id
    # disable the IRQ during debounce chec
    ch_prev.irq(handler=None)
    if stop_id != 0:
        stop_id -= 1
    # debounce time - ignore any activity during this period
    sleep(0.1)
    # re-enable the IRQ
    ch_prev.irq(trigger=Pin.IRQ_FALLING, handler = prev_btn_handler)  # change it to rising???
    
def next_btn_handler(pin, list_len):
    global stop_id
    # disable the IRQ during debounce chec
    ch_next.irq(handler=None)
    if stop_id < list_len:
        stop_id += 1
    # debounce time - ignore any activity during this period
    sleep(0.1)
    # re-enable the IRQ
    ch_next.irq(trigger=Pin.IRQ_FALLING, handler = next_btn_handler)  # change it to rising???
  
  
def chunks(lst, step):
    for i in range(0, len(lst), step):
        yield tuple(lst[i:i + step])
        
        
# enabling irq        
ch_prev.irq(trigger=Pin.IRQ_FALLING, handler = prev_btn_handler)
ch_next.irq(trigger=Pin.IRQ_FALLING, handler = next_btn_handler)

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
    

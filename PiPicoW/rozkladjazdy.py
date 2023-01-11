from get_bus import *
from get_display import *
# starting busstop id
stop_id = 1 
# defining input button pins for shifting stops
prev_btn = 2
next_btn = 3
# setting up the pins for shifting
ch_prev = Pin(prev_btn,Pin.IN, Pin.PULL_UP)
ch_next = Pin(next_btn,Pin.IN, Pin.PULL_UP)
how_many_stops = None

def prev_btn_handler(pin):
    global stop_id
    # disable the IRQ during debounce chec
    ch_prev.irq(handler=None)
    if stop_id != 0:
        stop_id -= 1
    sleep(1)    
    print("PRZERWANIE prev: ",stop_id)
    change_stop_sig("<")
    # debounce time - ignore any activity during this period
    # re-enable the IRQ
    ch_prev.irq(trigger=Pin.IRQ_RISING, handler = prev_btn_handler)
    
def next_btn_handler(pin):
    global stop_id
    if how_many_stops != None:  
        # disable the IRQ during debounce chec
        ch_next.irq(handler=None)
        if stop_id < (how_many_stops-1):
            stop_id += 1
        sleep(1)
        print("PRZERWANIE next: ",stop_id)
        change_stop_sig(">")
        # debounce time - ignore any activity during this period
        # re-enable the IRQ
        ch_next.irq(trigger=Pin.IRQ_RISING, handler = next_btn_handler)  # change it to rising???
  
  
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

how_many_stops = len(stops_list)
# enabling irq
ch_next.irq(trigger=Pin.IRQ_RISING, handler = next_btn_handler)
ch_prev.irq(trigger=Pin.IRQ_RISING, handler = prev_btn_handler)


# main loop
while True:
    while wlan.isconnected() == False:
        connect_aval_wlan(wifi_list,wlan)   
        sleep(2)        
    sleep(3)  # okres odświeżania
    bus_stop = get_and_display(stops_list, stop_id) # pobieranie danych z przystanku
    try:
        departures = bus_stop["Departures"]
        print(departures)
        print("stop_id",stop_id)
        print(bus_stop["Update"])
        # zamiana listy na listę tupli 3-elementowych
        dep = list(chunks(departures,3))[:5]
        print_board(dep,bus_stop["Update"],bus_stop["Name"]) 
    except:
        error_msg("AWARIA TABLICY",last_update_t())

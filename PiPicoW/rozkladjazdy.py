from get_bus import *
from get_display import *

# starting busstop id (IDs range from 0 tothe number of stops you input)
stop_id = 1 
# defining input button pins of microcontroller for shifting stops
prev_btn = 2
next_btn = 3
# setting up the pins for shifting
ch_prev = Pin(prev_btn,Pin.IN, Pin.PULL_UP)
ch_next = Pin(next_btn,Pin.IN, Pin.PULL_UP)

how_many_stops = None


def prev_btn_handler(pin):
    """
    Interrupt handler for pressing the "previous stop" button.
    
    """
    global stop_id
    # disable the IRQ during debounce check
    ch_prev.irq(handler=None)
    # debounce time - ignore any activity during this period
    sleep(1)
    # make graphic signal of stop change
    change_stop_sig("<")
    if stop_id != 0:
        stop_id -= 1
    print("PRZERWANIE prev: ",stop_id)    
    # re-enable the IRQ
    ch_prev.irq(trigger=Pin.IRQ_RISING, handler = prev_btn_handler)
    
def next_btn_handler(pin):
    """
    Interrupt handler for pressing the "next stop" button.
    
    """
    global stop_id
    if how_many_stops != None:  
        # disable the IRQ during debounce chec
        ch_next.irq(handler=None)
        # debounce time - ignore any activity during this period
        sleep(1)
        if stop_id < (how_many_stops-1):
            stop_id += 1
        print("PRZERWANIE next: ",stop_id)
        # make graphic signal of stop change
        change_stop_sig(">")
        # re-enable the IRQ
        ch_next.irq(trigger=Pin.IRQ_RISING, handler = next_btn_handler) 
  
  
def chunks(lst, step):
    """
    Yielding a list of elements, where every element is a list of {step} elements.
    @param: lst - list to divide into a list of lists
    @param: step - number of elements in the nested list
    
    """
    for i in range(0, len(lst), step):
        yield tuple(lst[i:i + step])
      
    
# cyclic interrupt for synhronising the local lime with ntp server every 7200000 ms (2 hours)
timer = Timer(period=7200000, mode=Timer.PERIODIC, callback=lambda t: set_time())
   

# reading networks list and wifi list from config file
with open('config.json', 'r') as f:
    data = json.load(f)
    wifi_list = data['networks']
    stops_list = data['transport_stop']

how_many_stops = len(stops_list)
# enabling irq
ch_next.irq(trigger=Pin.IRQ_RISING, handler = next_btn_handler)
ch_prev.irq(trigger=Pin.IRQ_RISING, handler = prev_btn_handler)

# starting message to ensure that the system is working
start_msg()
sleep(1)

# main loop
while True:
    while wlan.isconnected() == False:
        connect_aval_wlan(wifi_list,wlan)   
        sleep(2)        
    sleep(3)  # refresh time
    bus_stop = get_and_display(stops_list, stop_id) # pobieranie danych z przystanku
    try:
        departures = bus_stop["Departures"]
        print(departures)
        print("stop_id",stop_id)
        print(bus_stop["Update"])
        dep = list(chunks(departures,3))[:5]  # take only first 5 arrival times
        print_board(dep,bus_stop["Update"],bus_stop["Name"]) 
    except:
        error_msg("AWARIA TABLICY",last_update_t())


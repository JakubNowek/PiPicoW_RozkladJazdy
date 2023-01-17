# using library from https://github.com/rdagger/micropython-ili9341

import ili9341
import mySetup
from machine import Pin, SPI
from xglcd_font import XglcdFont
from time import sleep


led = Pin(21, Pin.OUT)  # pin 21 set high for additional 3.3V source
led.high()
display = mySetup.createMyDisplay()
unispace = XglcdFont('lib/fonts/Unispace12x24.c', 12, 24)

# definition of colors needed for display
def_color = {"Head": ili9341.color565(10, 200, 252),
             "First": ili9341.color565(0, 0, 200),
             "Middle": ili9341.color565(200, 200, 200),
             "Last": ili9341.color565(200, 20, 10),
             "Black":ili9341.color565(0,0,0) 
            }
    
    
def print_board(data,update,name):
    """
    Function responsible for printing bus stop data on the display.
    @param: data - data from bus stop to be printed
    @param: update - time of an update
    @param: name - name of the stop
    
    """
    name = '{:' '<15}'.format(name[:15])
    update = '{:' '>10}'.format(update)
    x = 0
    y = 0
    # define head
    text = "Linia Kierunek      Odjazd"
    display.draw_text(x, y, text, unispace,
                      def_color["Head"])  # ostatnia wyświetlana linia
    for line in data:
        y+=36
        if y==36:
            color = def_color["First"]
        elif y==72 or y==108 or y==144:
            color = def_color["Middle"]
        elif y==180:
            color = def_color["Last"]
            
        # read line
        linia, kierunek, odjazd = line[0], line[1], line[2]
        # line format
        text2 = '{:' '<3}'.format(linia[:3]) +\
                ' ' + '{:' '<11}'.format(kierunek[:11]) +\
                ' ' + '{:>9}'.format(odjazd[:9])
        display.draw_text(0, y , text2, unispace,
                          color)
    # display.fill_hrect(200, 216 ,119 ,24, def_color["Black"])
    # display stop name and time of update
    display.draw_text(0, 216 , name+update, unispace,
                          def_color["Head"])
                   
    
def change_stop_sig(direction):
    """
    Function responsible for signalising the stop change
    
    """
    display.fill_hrect(0, 216 ,319 ,24, def_color["Black"])
    display.draw_text(160, 216 , direction, unispace,
                          def_color["Head"])
    
    
def error_msg(msg):
    """
    Function displays an error message in the botom of display
    
    """
    display.fill_hrect(0, 216 ,319 ,24, def_color["Black"])
    display.draw_text(0, 216 , msg, unispace,
                          def_color["Head"])
    
    
def start_msg():
    """
    Function displays a start message
    
    """
    msg = "Turning on"
    display.clear()
    display.draw_text(160, 120 , msg, unispace,
                          def_color["Head"])
    sleep(1)
    display.clear()

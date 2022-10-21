# using library from https://github.com/rdagger/micropython-ili9341

import ili9341
import utime
import mySetup

from machine import Pin, SPI
from sys import implementation
from os import uname
from xglcd_font import XglcdFont
import re

led = Pin(21, Pin.OUT)
led.high()

print(implementation.name)
print(uname()[3])
print(uname()[4])

print(SPI(0))
print(SPI(1))

display = mySetup.createMyDisplay()

print('Loading fonts...')
print('Loading unispace')
unispace = XglcdFont('lib/fonts/Unispace12x24.c', 12, 24)
text = "Linia Kierunek      Odjazd"
line = "1"
direction = "Potulicka"
departure = "za 12 min"




display.clear()
display.draw_rectangle(0,0,320,240,100 )
display.draw_rectangle(0,0,300,200,200 )

def board(linia, kierunek, odjazd):
    text2 = '{:' '<3}'.format(linia[:3]) +\
            ' ' + '{:' '<11}'.format(kierunek[:11]) +\
            ' ' + '{:>9}'.format(odjazd[:9])
            
    display.draw_text(0, 0, text, unispace,
                      ili9341.color565(10, 200, 252))  # ostatnia wyświetlana linia
    display.draw_text(0, 36, text2, unispace,
                      ili9341.color565(0, 0, 200))
    display.draw_text(0, 72, text2, unispace,
                      ili9341.color565(200, 200, 200))
    display.draw_text(0, 108, text2, unispace,
                      ili9341.color565(200, 200, 200))
    display.draw_text(0, 144, text2, unispace,
                      ili9341.color565(200, 200, 200))
    display.draw_text(0, 180, text2, unispace,
                      ili9341.color565(200, 200, 200))
    display.draw_text(0, 216, text2, unispace,
                      ili9341.color565(200, 20, 10))  # ostatnia wyświetlana linia
    
for i in range(999):
    board(line, direction, departure)
    utime.sleep(3)
    line = f"{i}"
    
# for i in range(320):
#     display.scroll(i)
#     utime.sleep(0.02)
#     
# for i in range(320, 0, -1):
#     display.scroll(i)
#     utime.sleep(0.02)

# utime.sleep(0.5)
# # Display inversion on
# display.write_cmd(display.INVON)
# utime.sleep(2)
# # Display inversion off
# display.write_cmd(display.INVOFF)

while True:
    pass

print("- bye -")


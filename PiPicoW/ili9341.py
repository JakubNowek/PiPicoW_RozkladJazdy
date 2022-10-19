import ili934x as ili9341
from machine import Pin, SPI

led = Pin(21, Pin.OUT)
led.high()
spi = SPI(id=0, miso=Pin(16), mosi=Pin(19, Pin.OUT), sck=Pin(6, Pin.OUT))
display = ili9341.ILI9341(spi, cs=Pin(0), dc=Pin(5), rst=Pin(4))
display.fill(ili9341.color565(0xff, 0x11, 0x22))
display.print('text\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\ntext\n')

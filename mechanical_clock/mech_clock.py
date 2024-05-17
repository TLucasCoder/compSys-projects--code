from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_LCD_240X240, PEN_RGB332, DISPLAY_LCD_160X80
import utime
from machine import Pin, Timer, ADC
from machine import SPI,PWM
from pimoroni_bus import SPIBus
import cmath
import framebuf
import os

BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9


class LCD_1inch3(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 240
        self.height = 240
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,100000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width) #Due to insufficient memory, the screen is displayed twice
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        
        self.red   =   0x07E0
        self.green =   0x001f
        self.blue  =   0xf800
        self.white =   0xffff
        self.black =   0x0000
        
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize dispaly"""  
        self.rst(1)
        self.rst(0)
        self.rst(1)
        
        self.write_cmd(0x36)
        self.write_data(0x70)

        self.write_cmd(0x3A) 
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xB7)
        self.write_data(0x35) 

        self.write_cmd(0xBB)
        self.write_data(0x19)

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x12)   

        self.write_cmd(0xC4)
        self.write_data(0x20)

        self.write_cmd(0xC6)
        self.write_data(0x0F) 

        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(0xE0)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0D)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2B)
        self.write_data(0x3F)
        self.write_data(0x54)
        self.write_data(0x4C)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x1F)
        self.write_data(0x23)

        self.write_cmd(0xE1)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0C)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2C)
        self.write_data(0x3F)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x2F)
        self.write_data(0x1F)
        self.write_data(0x1F)
        self.write_data(0x20)
        self.write_data(0x23)
        
        self.write_cmd(0x21)

        self.write_cmd(0x11)

        self.write_cmd(0x29)

    def show(self,Xstart,Ystart,Xend,Yend):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(Xstart & 0xFF)
        self.write_data(0x00)
        self.write_data((Xend - 1) & 0xFF)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(Ystart & 0xFF)
        self.write_data(0x00)
        self.write_data((Yend - 1) & 0xFF)
        
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)

  
if __name__=='__main__':
    LCD = LCD_1inch3()


adcpin = 4
sensor = machine.ADC(adcpin)

page_tracker = 0
# the spibus for the display: pico-LCD-1.3
spibus = SPIBus(cs = 9, sck = 10, mosi = 11, dc = 8, bl = 13)
# Setting up the display
display = PicoGraphics(display = DISPLAY_LCD_240X240, bus=spibus, pen_type=PEN_RGB332)
display.set_font("bitmap8")

# Get the display size
width = 240
height = 240

# Set up the buttons
button_a = Pin(15, Pin.IN, Pin.PULL_UP)
button_b = Pin(17, Pin.IN, Pin.PULL_UP)
button_x = Pin(19, Pin.IN, Pin.PULL_UP)
button_y = Pin(21, Pin.IN, Pin.PULL_UP)

# Setting up colours
WHITE  = display.create_pen(255, 255, 255)
BLACK  = display.create_pen(0, 0, 0)
RED    = display.create_pen(255, 0, 0)
DARK_RED = display.create_pen(139, 0, 0)
YELLOW = display.create_pen(255, 255, 0)
LIGHT_GREY   = display.create_pen(138, 163, 186)
GREEN  = display.create_pen(0, 255, 0)
GREY = display.create_pen(66, 66, 66)

# Keep track of the hour offset
hour_offset = 0

def display_time():
    time = utime.localtime()
    hour = (time[3] + hour_offset) % 24
    minute = time[4]
    second = time[5]
    # Format the time as a string
    time_str = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
    # centering the position of the text
    text_width = len(time_str) * 20
    text_height = 25
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    display.set_pen(BLACK)
    display.clear()
    # Display the time
    display.set_pen(WHITE)
    display.text(time_str, x, y, width, 5)

def drawClock():
    display.set_pen(LIGHT_GREY)
    display.rectangle(158,103,40, 40)
    display.set_pen(GREY)
    display.rectangle(160,105,35, 35)
    
    time = utime.localtime()
    day = time[2]
    hour = (time[3] + hour_offset) % 24
    minute = time[4]
    second = time[5]
    display.set_pen(WHITE)
    day_str = "{}".format(day)
    display.text(day_str,165,113, width,3)
    for x in range(60):
        hour_pos = hour * 5 + minute // 12
        hour_pos = hour_pos % 60
        if(x == second):
            x1 = 120 + 110 * cmath.sin((x)* cmath.pi/30)
            y1 = 120 - 110 * cmath.cos((x)* cmath.pi/30)
            xr1 = x1.real
            yr1 = y1.real
            display.set_pen(RED)
            display.line(120, 120 ,int(xr1) , int(yr1), 3)  
        if(x == minute):
            x1 = 120 + 85 * cmath.sin((x)* cmath.pi/30)
            y1 = 120 - 85 * cmath.cos((x)* cmath.pi/30)
            xr1 = x1.real
            yr1 = y1.real
            display.set_pen(WHITE)
            display.line(120, 120 ,int(xr1) , int(yr1), 5)  
        if(x == hour_pos):
            x1 = 120 + 60 * cmath.sin((x)* cmath.pi/30)
            y1 = 120 - 60 * cmath.cos((x)* cmath.pi/30)
            xr1 = x1.real
            yr1 = y1.real
            display.set_pen(GREEN)
            display.line(120, 120 ,int(xr1) , int(yr1), 5) 
    
        

def clockShape():
    # Clear the screen
    display.set_pen(BLACK)
    display.clear()
    display.set_pen(DARK_RED)
    display.circle(120, 120, 110)
    display.set_pen(BLACK)
    display.circle(120, 120, 100)
    display.set_pen(YELLOW)
    for x in range(12):
        
        x1 = 120 + 110 * cmath.sin((x)* cmath.pi/6)
        y1 = 120 - 110 * cmath.cos((x)* cmath.pi/6)
        x2 = 120 + 95 * cmath.sin((x)* cmath.pi/6)
        
        y2 = 120 - 95 * cmath.cos((x)* cmath.pi/6)
        xr1 = x1.real
        xr2 = x2.real
        yr1 = y1.real
        yr2 = y2.real
        # cmath.sqrt((x2-120)**2 + (y2-120)**2) = 120
        display.set_pen(YELLOW)
        display.line(int(xr2), int(yr2) ,int(xr1) , int(yr1), 3)
        drawClock()

def display_date():
    date = utime.localtime()
    year = date[0]
    month = date[1]
    day = date[2]
    
    # You can adjust the position and format of the date text as needed
    date_str = "{}/{}/{}".format(day, month, year)
    display.set_pen(BLACK)
    display.clear()
    display.set_pen(RED)  # Set pen color for date
    display.text(date_str, 40, 100,width, 4)  # Display datea

def getTemp():
    adc_value = sensor.read_u16()
    volt = (3.3/65535) * adc_value
    temperature = 27 - (volt - 0.706)/0.001721
    display.set_pen(BLACK)
    display.clear()
    temperature = round(temperature,2)
    temp = "{}".format(temperature)
    temp = temp + chr(176) + "C"
    display.set_pen(RED)
    display.text(temp, 50, 100, width, 5) 


def setPageTracker(pin):
    global page_tracker
    if (button_x() == 0):   
        page_tracker = 1
    elif (button_y() == 0):
        page_tracker = 0
    elif (button_b() == 0):
        page_tracker = 2
    else :
        page_tracker = 3

    
# Set up the buttons with interrupts
button_x.irq(handler = setPageTracker , trigger= Pin.IRQ_FALLING)
button_y.irq( handler=setPageTracker, trigger= Pin.IRQ_FALLING)
button_b.irq( handler=setPageTracker, trigger= Pin.IRQ_FALLING)
button_a.irq( handler=setPageTracker, trigger= Pin.IRQ_FALLING)


# Main loop
while True:
    if (page_tracker == 0):
        clockShape()     
    elif (page_tracker == 1):
        getTemp()
    elif (page_tracker == 2):
        display_date()
    else:
        display_time()
    display.update()
    utime.sleep(1)  # pause for 1 second before updating the time again
    

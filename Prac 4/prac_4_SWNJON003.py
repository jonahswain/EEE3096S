# =======================
# EEE3096S Prac 4
# 01/09/2018
# Jonah Swain [SWNJON003]
# 
# =======================

# IMPORTS
import time
import datetime
import RPi.GPIO as GPIO
import Adafruit_MCP3008
import threading
import spidev

# CLASSES
class Timer():
    """A basic timer - tracks how much time has elapsed"""

    def __init__(self):
        self.start_time = time.time()

    def get_time(self):
        return time.strftime("%H:%M:%S", time.gmtime(time.time() - self.start_time))

    def reset(self):
        self.start_time = time.time()

class AnalogDevice():
    """A generic analog device connected to an MCP3008 channel"""

    def __init__(self, mcp3008, channel, differential=False):
        self.adc = mcp3008
        self.adcch = channel
        self.diff = differential

    def get_value(self):
        if (self.diff):
            return self.adc.read_adc_difference(self.adcch)
        else:
            return self.adc.read_adc(self.adcch)

class Potentiometer(AnalogDevice):
    """A potentiometer"""

    def __init__(self, mcp3008, channel):
        super().__init__(mcp3008, channel)

    def get_value(self):
        return (str("{0:.1f}".format(3.3*(super().get_value()/1023))) + " V")

class TempSensor(AnalogDevice):
    """A temperature sensor"""

    def __init__(self, mcp3008, channel):
        super().__init__(mcp3008, channel)

    def get_value(self):
        return (str(int((super().get_value()-155)/3.1)) + "°C")


class LightSensor(AnalogDevice):
    """An LDR based light sensor"""

    low_calibration = 230
    high_calibration = 780

    def __init__(self, mcp3008, channel):
        super().__init__(mcp3008, channel)

    def get_value(self):
        light_value = ((super().get_value() - LightSensor.low_calibration)/(LightSensor.high_calibration - LightSensor.low_calibration))*100
        if (light_value > 100):
            light_value = 100
        elif (light_value < 0):
            light_value = 0
        return (str(int(light_value)) + " %")



class Prac4(threading.Thread):
    """The main practical class"""

    header = "Time      Timer     Pot    Temp  Light "
    row_length = 39
    time_length = 10
    timer_length = 10
    pot_length = 7
    temp_length = 7
    light_length = 5

    reset_pin = 17
    frequency_pin = 18
    stop_pin = 27
    display_pin = 22

    def clear_console():
        print("\n"*50)

    def generate_row(time_val, timer_val, pot_val, temp_val, light_val):
        return (time_val + " "*(Prac4.time_length - len(time_val)) + timer_val + " "*(Prac4.timer_length - len(timer_val)) + pot_val + " "*(Prac4.pot_length - len(pot_val)) + temp_val + " "*(Prac4.temp_length - len(temp_val)) + light_val + " "*(Prac4.light_length - len(light_val)))

    def print_row(row):
        print(row)
        print("-"*Prac4.row_length)

    def print_header():
        print("-"*Prac4.row_length)
        print(Prac4.header)
        print("-"*Prac4.row_length)

    def get_time():
        return time.strftime("%H:%M:%S", time.localtime(time.time()))

    def __init__(self):
        threading.Thread.__init__(self)
        self.stopped = False
        #self.spi = spidev.SpiDev()
        #self.spi.open(0, 0)
        self.adc = Adafruit_MCP3008.MCP3008(mosi = 20, miso = 19, clk = 21, cs = 8)
        
    def run(self): # Thread run method
        # Setup
        Prac4.clear_console()
        Prac4.print_header()
        self.row_buffer = []

        self.timer = Timer()
        self.pot = Potentiometer(self.adc, 0)
        self.temp = TempSensor(self.adc, 1)
        self.light = LightSensor(self.adc, 2)

        self.delay = 0.5

        # GPIO setup
        GPIO.setup(Prac4.reset_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.add_event_detect(Prac4.reset_pin, GPIO.FALLING, callback = self.reset_sw, bouncetime = 100)
        GPIO.setup(Prac4.frequency_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.add_event_detect(Prac4.frequency_pin, GPIO.FALLING, callback = self.frequency_sw, bouncetime = 100)
        GPIO.setup(Prac4.stop_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.add_event_detect(Prac4.stop_pin, GPIO.FALLING, callback = self.stop_sw, bouncetime = 100)
        GPIO.setup(Prac4.display_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.add_event_detect(Prac4.display_pin, GPIO.FALLING, callback = self.display_sw, bouncetime = 100)

        # Main loop
        while(True):
            row = Prac4.generate_row(Prac4.get_time(), self.timer.get_time(), self.pot.get_value(), self.temp.get_value(), self.light.get_value())
            if (self.stopped):
                if (len(self.row_buffer) <= 5):
                    self.row_buffer.append(row)
            else:
                Prac4.print_row(row)
            time.sleep(self.delay)
                    

    def reset_sw(self, channel): # Reset button pressed
        self.timer.reset()
        Prac4.clear_console()
        Prac4.print_header()

    def frequency_sw(self, channel): # Frequency button pressed
        if(self.delay == 0.5):
            self.delay = 1
        elif(self.delay == 1):
            self.delay = 2
        elif(self.delay == 2):
            self.delay = 0.5

    def stop_sw(self, channel): # Stop button pressed
        self.stopped = not self.stopped
        self.row_buffer = []

    def display_sw(self, channel): # Display button pressed
        if (self.stopped):
            Prac4.clear_console()
            Prac4.print_header()
            for r in self.row_buffer:
                Prac4.print_row(r)


# FUNCTIONS


# MAIN FUNCTION
def main():
    GPIO.setmode(GPIO.BCM)
    # Run the prac
    prac = Prac4()
    prac.start()

if (__name__ == "__main__"): # Run main if script is being executed as main
    main()
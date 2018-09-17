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
        return (str("{0:.2f}".format(3.3*(super().get_value()/1023))) + " V")

class TempSensor(AnalogDevice):
    """A temperature sensor"""

    def __init__(self, mcp3008, channel):
        super().__init__(mcp3008, channel)

    def get_value(self):
        return (str(int((super().get_value()-155)/3.1)) + " °C")


class LightSensor(AnalogDevice):
    """An LDR based light sensor"""

    low_calibration = 0
    high_calibration = 1023

    def __init__(self, mcp3008, channel):
        super().__init__(mcp3008, channel)

    def get_value(self):
        light_value = ((super().get_value() - LightSensor.low_calibration)/(LightSensor.high_calibration - LightSensor.low_calibration))*100
        return (str(int(light_value)) + " %")



class Prac4(threading.Thread):
    """The main practical class"""

    def __init__(self):
        threading.Thread.__init__(self)

    def reset_sw(self): # Reset button pressed
        pass

    def frequency_sw(self): # Frequency button pressed
        pass

    def stop_sw(self): # Stop button pressed
        pass

    def display_sw(self): # Display button pressed
        pass




# FUNCTIONS


# MAIN FUNCTION
def main():
    pass

if (__name__ == "__main__"): # Run main if script is being executed as main
    main()
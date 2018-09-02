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

# CLASSES
class Timer():
    """A basic timer - tracks how much time has elapsed"""

    def __init__(self):
        pass

    def get_time(self):
        pass

class AnalogDevice():
    """A generic analog device connected to an MCP3008 channel"""

    def __init__(self, mcp3008, channel, differential=False):
        self.adc = mcp3008
        self.adcch = channel
        self.diff = differential

    def get_value(self):
        pass

class Potentiometer(AnalogDevice):
    """A potentiometer"""

    def __init__(self, mcp3008, channel):
        super().__init__(mcp3008, channel)

    def get_value(self):
        pass

class TempSensor(AnalogDevice):
    """A potentiometer"""

    def __init__(self, mcp3008, channel):
        super().__init__(mcp3008, channel)

    def get_value(self):
        pass


class LightSensor(AnalogDevice):
    """A potentiometer"""

    def __init__(self, mcp3008, channel):
        super().__init__(mcp3008, channel)

    def get_value(self):
        pass


# FUNCTIONS


# MAIN FUNCTION
def main():
    pass

if (__name__ == "__main__"): # Run main if script is being executed as main
    main()
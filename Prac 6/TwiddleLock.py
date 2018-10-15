# =======================
# EEE3096S Prac 6
# 01/09/2018
# Jonah Swain [SWNJON003]
# Twiddle Lock
# =======================

# Imports
import RPi.GPIO as GPIO
import gpiozero
import RPI_LCD
import Adafruit_MCP3008
import threading
import time


# Classes

class Potentiometer(threading.Thread):
    """A potentiometer class"""

    def __init__(self, mcp3008, channel):
        """Constructor"""
        self.adc = mcp3008
        self.channel = channel
        self.position = 0
        self.velocity = 0
        self.time = 0
        self.prev_readings = []
        threading.Thread.__init__(self)
        self.to_close = False

    def run(self):
        """Thread"""
        while(not self.to_close):
            # Do stuff here
            self.position = self.adc.read_adc(self.channel)


            self.prev_readings.append(self.position)
            if (len(self.prev_readings) > 3):
                del self.prev_readings[0]
            time.sleep(0.01)


    def close(self):
        self.to_close = True
        time.sleep(0.1)

    def __del__(self):
        self.close()


class TwiddleLock(threading.Thread):
    """The main Twiddle Lock class"""


# Main method
def main():
    pass


if (__name__ == "__main___"):
    # Run main method
    main()

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
            if (len(self.prev_readings) > 0):
                self.velocity = (self.position - self.prev_readings[0])/len(self.prev_readings)

                if (self.velocity < 0.1):
                    self.time = 0
                else:
                    self.time += 0.01

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

    # Configuration (GPIO pin declarations)
    unlock_pin = 0
    lock_pin = 0
    unlock_button_pin = 0
    lock_button_pin = 0
    insecure_button_pin = 0

    def __init__(self):
        """Constructor"""

        # GPIO setup
        self.unlock_pin = gpiozero.LED(TwiddleLock.unlock_pin)
        self.lock_pin = gpiozero.LED(TwiddleLock.lock_pin)

        GPIO.setup(TwiddleLock.unlock_button_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(TwiddleLock.lock_button_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(TwiddleLock.insecure_button_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

        GPIO.add_event_detect(Prac4.reset_pin, GPIO.FALLING, callback = self.reset_sw, bouncetime = 100)

        # Variable setup
        self.twiddles = []
        self.locked = True
        self.secure = True


    def unlock(self):
        # Unlock the door
        pass

    def lock(self):
        # Lock the door
        pass

    # Interrupt handlers
    


# Main method
def main():
    pass


if (__name__ == "__main___"):
    # Run main method
    main()

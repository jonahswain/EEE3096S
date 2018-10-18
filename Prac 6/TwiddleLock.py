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

class Combination():
    """A Combination (consisting of directions/durations)"""

    def __init__(self, arr_time, arr_direction):
        self.combination = []
        if (len(arr_time) == len(arr_direction) and (len(arr_time) > 0)): # Check for valid equal length time/direction arrays
            for i in range(len(arr_time)):
                self.combination.append([arr_direction[i], arr_time[i]])
        else:
            raise RuntimeError("Invalid arguments for Combination")


    def __eq__(self, other):
        if (not isinstance(other, Combination)):
            return False

        if (len(self.combination) != len(other.combination)):
            return False

        for i in range(len(self.combination)):
            if ((self.combination[i][0] != other.combination[i][0]) or (self.combination[i][1] != other.combination[i][1])):
                return False

        return True



class Potentiometer(threading.Thread):
    """A potentiometer class"""

    def __init__(self, mcp3008, channel):
        """Constructor"""
        self.adc = mcp3008
        self.channel = channel
        self.position = 0
        self.velocity = 0
        self.prev_readings = []
        threading.Thread.__init__(self)
        self.to_close = False

    def run(self):
        """Thread"""
        while(not self.to_close):
            # Do stuff here
            self.position = self.adc.read_adc(self.channel)
            self.prev_readings.append(self.position)
            if (len(self.prev_readings) > 4):
                del self.prev_readings[0]
            if (len(self.prev_readings) > 0):
                self.velocity = 0
                for i in range(1, len(self.prev_readings)):
                    self.velocity += self.prev_readings[-i] - self.prev_readings[-i -1]
                self.velocity /= (len(self.prev_readings) - 1)
                if (abs(self.velocity) < 0.1):
                    self.velocity = 0

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
    service_btn_pin = 0

    spi_mosi_pin = 20
    spi_miso_pin = 19
    spi_clk_pin = 21
    spi_ss_pin = 8
    adc_pot_channel = 0


    def __init__(self):
        """Constructor"""

        threading.Thread.__init__(self) # Parent class constructor

        # GPIO setup
        self.unlock_pin = gpiozero.LED(TwiddleLock.unlock_pin)
        self.lock_pin = gpiozero.LED(TwiddleLock.lock_pin)
        self.service_btn = gpiozero.Button(TwiddleLock.service_btn_pin, bounce_time = 0.2, hold_time = 3)

        # Potentiometer setup
        self.adc = Adafruit_MCP3008.MCP3008(mosi = TwiddleLock.spi_mosi_pin, miso = TwiddleLock.spi_miso_pin, clk = TwiddleLock.spi_clk_pin, cs = TwiddleLock.spi_ss_pin)
        self.potentiometer = Potentiometer(self.adc, TwiddleLock.adc_pot_channel)

        # Variable setup
        self.log = []
        self.dir = []
        self.locked = True
        self.secure = True
        self.combo_in_progress = False


    def run(self):
        """Thread"""

    def unlock(self):
        # Unlock the door
        pass

    def lock(self):
        # Lock the door
        pass

    def failed_unlock_attempt(self):
        # Failed unlock attempt (wrong code)
        pass

    # Interrupt handlers
    def service_btn_pressed(self):
        pass

    def service_btn_held(self):
        pass


# Main method
def main():
    pass


if (__name__ == "__main__"):
    # Run main method
    main()

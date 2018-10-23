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

    comparison_error_threshhold = 4

    def __init__(self, arr_time, arr_direction):
        self.combination = []
        if (len(arr_time) == len(arr_direction) and (len(arr_time) > 0)): # Check for valid equal length time/direction arrays
            for i in range(len(arr_time)):
                self.combination.append([arr_direction[i], arr_time[i]])
        else:
            raise RuntimeError("Invalid arguments for Combination")


    def __eq__(self, other): # Secure comparison
        if (not isinstance(other, Combination)):
            return False

        if (len(self.combination) != len(other.combination)):
            return False

        for i in range(len(self.combination)):
            if ((self.combination[i][0] != other.combination[i][0]) or (abs(self.combination[i][1] - other.combination[i][1]) > Combination.comparison_error_threshhold)):
                return False

        return True

    def comp_unsecure(self, other): # Unsecure comparison
        if (not isinstance(other, Combination)):
            return False

        if (len(self.combination) != len(other.combination)):
            return False

        log_1 = []
        log_2 = []

        for i in range(len(self.combination)):
            log_1.append(self.combination[i][1])
            log_2.append(other.combination[i][1])

        log_1.sort()
        log_2.sort()

        for i in range(len(self.combination)):
            if (abs(log_1[i] - log_2[i]) > Combination.comparison_error_threshhold):
                return False

        return True
        

    def __str__(self):
        # To string
        outstr = ""
        for i in range(len(self.combination)):
            if (self.combination[i][0] > 0):
                outstr = outstr + "R"
            else:
                outstr = outstr + "L"
            outstr = outstr + str(self.combination[i][1])
        return outstr



class Potentiometer(threading.Thread):
    """A potentiometer class"""

    def __init__(self, mcp3008, channel):
        """Constructor"""
        self.adc = mcp3008
        self.channel = channel
        self.position = 0
        self.velocity = 0
        self.prev_reading = 0
        threading.Thread.__init__(self)
        self.to_close = False

    def run(self):
        """Thread"""
        while(not self.to_close):
            # Do stuff here
            self.position = self.adc.read_adc(self.channel)
            self.velocity = self.position - self.prev_reading
            self.prev_reading = self.position
            if (abs(self.velocity) < 5):
                self.velocity = 0

            time.sleep(0.05)


    def close(self):
        self.to_close = True
        time.sleep(0.1)

    def __del__(self):
        self.close()


class TwiddleLock(threading.Thread):
    """The main Twiddle Lock class"""

    # Configuration (GPIO pin declarations)
    unlock_pin = 16
    lock_pin = 6
    service_btn_pin = 26
    buzzer_pin = 12

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
        self.buzzer = gpiozero.Buzzer(TwiddleLock.buzzer_pin)

        # Potentiometer setup
        self.adc = Adafruit_MCP3008.MCP3008(mosi = TwiddleLock.spi_mosi_pin, miso = TwiddleLock.spi_miso_pin, clk = TwiddleLock.spi_clk_pin, cs = TwiddleLock.spi_ss_pin)
        self.potentiometer = Potentiometer(self.adc, TwiddleLock.adc_pot_channel)
        self.potentiometer.start()

        # LCD screen setup
        self.lcd = RPI_LCD.LCD(18, 17, 27, 22, 23, 24)

        # Variable setup
        self.log = []
        self.dir = []
        self.service_btn_held_last = False
        self.locked = True
        self.secure = True
        self.combo_in_progress = False
        self.to_close = False

        self.correct_combo = Combination([10, 20, 10], [-1, 1, -1])


    def run(self):
        """Thread"""

        self.lcd.initialise() # Setup the LCD
        self.lcd.write("Twiddle Lock", "")

        self.lock() # Lock the door

        self.current_direction = 0
        self.current_time = 0
        self.prev_direction = 0
        self.stationary = False
        self.stationary_time = 0

        self.service_btn_held_time = 0

        while(True):
            # Main loop
            if (self.combo_in_progress):
                self.prev_direction = self.current_direction
                if (self.potentiometer.velocity > 0):
                    self.current_direction = 1
                    self.stationary = False
                elif (self.potentiometer.velocity < 0):
                    self.current_direction = -1
                    self.stationary = False
                else:
                    self.stationary = True

                if (self.stationary_time > 10):
                    self.current_direction = 0

                if (self.current_direction != self.prev_direction):
                    if (self.prev_direction != 0):
                        if (self.current_time > 2):
                            self.log.append(self.current_time)
                            self.dir.append(self.prev_direction)
                    self.current_time = 0

                if (self.stationary_time > 20):
                    self.combo_in_progress = False
                    if (len(self.log) > 0):
                        self.combo = Combination(self.log, self.dir)
                        print("Combination entered: ", self.combo)
                        if (self.secure):
                            if (self.combo == self.correct_combo):
                                self.unlock()
                            else:
                                self.failed_unlock_attempt()
                        else:
                            if (self.combo.comp_unsecure(self.correct_combo)):
                                self.unlock()
                            else:
                                self.failed_unlock_attempt()

                if (not self.stationary):
                    self.current_time += 1
                    self.stationary_time = 0
                else:
                    self.stationary_time += 1
            else:
                self.current_time = 0
                self.current_direction = 0

            if (self.service_btn.is_pressed):
                self.service_btn_held_time += 0.1
            else:
                if (self.service_btn_held_time > 3):
                    self.service_btn_held()
                elif (self.service_btn_held_time > 0.3):
                    self.service_btn_pressed()
                self.service_btn_held_time = 0

            time.sleep(0.1)


    def unlock(self):
        # Unlock the door
        self.locked = False
        self.unlock_pin.blink(2, 0, 1) # Pulse the unlock line for 2s
        self.buzzer.beep(2, 0, 1) # Beep the buzzer for 2 sec
        if (self.secure):
            self.lcd.write("Twiddle Lock", "Unlocked")
        else:
            self.lcd.write("Unsecure Lock", "Unlocked")

    def lock(self):
        # Lock the door
        self.locked = True
        self.lock_pin.blink(2, 0, 1) # Pulse the lock line for 2s
        self.buzzer.beep(0.15, 0.15, 2) # Beep the buzzer twice quickly
        if (self.secure):
            self.lcd.write("Twiddle Lock", "Locked")
        else:
            self.lcd.write("Unsecure Lock", "Locked")

    def failed_unlock_attempt(self):
        # Failed unlock attempt (wrong code)
        self.buzzer.beep(0.5, 0.5, 3) # Beep the buzzer three times
        if (self.secure):
            self.lcd.write("Twiddle Lock", "Wrong Combo")
        else:
            self.lcd.write("Unsecure Lock", "Wrong Combo")
        time.sleep(3)
        if (self.secure):
            self.lcd.write("Twiddle Lock", "Locked")
        else:
            self.lcd.write("Unsecure Lock", "Locked")

    # Interrupt handlers
    def service_btn_pressed(self):
        self.log = []
        self.dir = []
        if (not self.combo_in_progress):
            self.combo_in_progress = True
            self.current_direction = 0
            self.prev_direction = 0
            self.current_time = 0
            self.stationary = False
            self.stationary_time = 0
            if (self.secure):
                self.lcd.write("Twiddle Lock", "Enter combo")
            else:
                self.lcd.write("Unsecure Lock", "Enter combo")
        if (not self.locked):
            self.lock()


    def service_btn_held(self):
        self.secure = not self.secure
        if (self.secure):
            if (self.locked):
                self.lcd.write("Twiddle Lock", "Locked")
            else:
                self.lcd.write("Twiddle Lock", "Unlocked")
        else:
            if (self.locked):
                self.lcd.write("Unsecure Lock", "Locked")
            else:
                self.lcd.write("Unsecure Lock", "Unlocked")

    def close(self):
        self.to_close = True

    def __del__(self):
        self.close()
        time.sleep(0.2)


# Main method
def main():
    twiddle_lock = TwiddleLock()
    twiddle_lock.start()


if (__name__ == "__main__"):
    # Run main method
    main()

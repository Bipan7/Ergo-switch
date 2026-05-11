# gpio_handler.py

try:
    import RPi.GPIO as GPIO
    RPI_AVAILABLE = True
except ImportError:
    # Allows code to run on laptop (no Raspberry Pi)
    RPI_AVAILABLE = False


class GPIOHandler:
    def __init__(self, button_pin=17, led_pin=27):
        self.button_pin = button_pin
        self.led_pin = led_pin

        if RPI_AVAILABLE:
            GPIO.setmode(GPIO.BCM)

            GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.led_pin, GPIO.OUT)

    def read_button(self):
        if not RPI_AVAILABLE:
            return False

        return GPIO.input(self.button_pin) == 0  # pressed

    def set_led(self, state):
        if not RPI_AVAILABLE:
            return

        GPIO.output(self.led_pin, GPIO.HIGH if state else GPIO.LOW)

    def cleanup(self):
        if RPI_AVAILABLE:
            GPIO.cleanup()
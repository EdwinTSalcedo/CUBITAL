import RPi.GPIO as GPIO
import time

# Use Broadcom SOC Pin numbers
GPIO.setmode(GPIO.BCM)

# Pin to be used for LED/PWM
pin = 12

# Set up the GPIO pin as an output
GPIO.setup(pin, GPIO.OUT)

try:
    for i in range(10):
        # Turn the pin on
        GPIO.output(pin, GPIO.HIGH)
        print("Pin 12 is ON")
        time.sleep(3)  # Wait for 3 seconds

        # Turn the pin off
        GPIO.output(pin, GPIO.LOW)
        print("Pin 12 is OFF")
        time.sleep(3)  # Wait for 3 seconds

finally:
    # Clean up the GPIO to reset pin configuration
    GPIO.cleanup()
# External module imports
import RPi.GPIO as GPIO
import time

print("Hello LED")

leds = [27,21,18,12,25,23,20,16]
#leds = [16]
print("Setting Broadcom Mode")
# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme

for led in leds:
    GPIO.setup(led, GPIO.OUT) 

print("Here we go! Press CTRL+C to exit")
try:
    while 1:
            print ("OFF");
            
            for led in leds:
                GPIO.output(led, GPIO.LOW)
            time.sleep(1.00)
            
            print ("ON");            
            
            for led in leds:
                GPIO.output(led, GPIO.HIGH)
            time.sleep(1) 
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup() # cleanup all GPIO

# External module imports
import RPi.GPIO as GPIO
import time

print("Hello LED")

ledPin = 14
ledArray = [7,8,9,10,11]

print("Setting Broadcom Mode")
# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme

for led in ledArray:
    GPIO.setup(led, GPIO.OUT) 

print("Here we go! Press CTRL+C to exit")
try:
    while 1:
            print ("OFF");
            
            for led in ledArray:
                GPIO.output(led, GPIO.LOW)
            time.sleep(1.00)
            
            print ("ON");            
            
            for led in ledArray:
                GPIO.output(led, GPIO.HIGH)
            time.sleep(1) 
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup() # cleanup all GPIO

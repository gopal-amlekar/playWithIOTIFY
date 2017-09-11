# External module imports
import RPi.GPIO as GPIO
import time

print("Hello Button")


leds = [7,8,9,10,11,22,23,24]
buttons = [14,15,17,18]

print("Setting Broadcom Mode")
# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme

for led in leds:
	GPIO.setup(led, GPIO.OUT)
	
for btn in buttons:
	GPIO.setup(btn, GPIO.IN)

time.sleep(0.5) 
counter = 0;

try:
    while 1:
        for btnIndex in xrange(0, len(buttons)):
			if (GPIO.input(buttons[btnIndex])):
				GPIO.output(leds[(btnIndex * 2)], GPIO.HIGH)
				GPIO.output(leds[(btnIndex * 2) + 1], GPIO.HIGH)
			else:
				GPIO.output(leds[(btnIndex * 2)], GPIO.LOW)
				GPIO.output(leds[(btnIndex * 2) + 1], GPIO.LOW)
				
        time.sleep(0.1) 
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup() # cleanup all GPIO

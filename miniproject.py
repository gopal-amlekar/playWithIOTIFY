import RPi.GPIO as GPIO
import time
import numpy as np
STEP_PIN = 7
DIR_PIN = 8
M1_PIN = 9
M0_PIN = 10

NSLEEP_PIN = 11
NFAULT_PIN = 14
NENBL_PIN = 15
CONFIG_PIN = 17

TRIG = 5
ECHO = 6

steps = 20
micro_step = 1.0 #Possible values: 1.0, 1.0/2, 1.0/4, 1.0/8, 1.0/16, 1.0/32 


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


print "Autonomous Robot simulation"

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.setup(STEP_PIN, GPIO.OUT)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(NSLEEP_PIN, GPIO.OUT)
GPIO.setup(NFAULT_PIN, GPIO.IN)
GPIO.setup(NENBL_PIN, GPIO.OUT)
GPIO.setup(CONFIG_PIN, GPIO.OUT)


GPIO.output(NSLEEP_PIN, False)  #Low power and reset all logic
GPIO.output(CONFIG_PIN, True)   #Indexer mode
GPIO.output(NSLEEP_PIN, True)   #Enable device

while GPIO.input(NFAULT_PIN)==0:
	time.sleep(0.001)

GPIO.output(NENBL_PIN, False) #Enable all outputs

if steps < 0:
	GPIO.output(DIR_PIN, False) #Anticlockwise
	steps = -steps             
else:
	GPIO.output(DIR_PIN, True)  #Clockwise

GPIO.setup(M1_PIN, GPIO.OUT)
GPIO.output(M1_PIN, False)
GPIO.setup(M0_PIN, GPIO.OUT)
GPIO.output(M0_PIN, False)
        
while True:
    GPIO.output(TRIG, False)
    time.sleep(2)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    
            
    while GPIO.input(ECHO)==0:
      pulse_start = time.time()
    
    while GPIO.input(ECHO)==1:
      pulse_end = time.time()
    
    pulse_duration = pulse_end - pulse_start
    
    distance = pulse_duration * 17150
    
    distance = round(distance, 2)
    
    print "Distance:",distance,"cm"
    
    if (distance < 20):
    	for count in np.arange(0, steps, micro_step):
    		time.sleep(0.05)
    		GPIO.output(STEP_PIN, True) # High going pulse moves the motor
    		time.sleep(0.05)
    		GPIO.output(STEP_PIN, False)
    		
    	    #sys.stdout.write(".")
    	    #sys.stdout.flush()

GPIO.cleanup()
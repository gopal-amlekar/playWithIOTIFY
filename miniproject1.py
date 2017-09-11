import smbus
import RPi.GPIO as GPIO
import numpy as np
import time

SHT21_ADD = 0x40
SHT21_STATUS_MASK = 0xFFFC

SHT21_MEASURE_TEMP_CMD = 0xF3
SHT21_MEASURE_HUM_CMD = 0xF5

STEP_PIN = 7
DIR_PIN = 8
M1_PIN = 9
M0_PIN = 10

NSLEEP_PIN = 11
NFAULT_PIN = 14
NENBL_PIN = 15
CONFIG_PIN = 17


def get_temperature():
    bus.write_byte(SHT21_ADD, SHT21_MEASURE_TEMP_CMD)

    time.sleep(0.1)

    temp_msb = bus.read_byte (SHT21_ADD)
    #print temp_msb
    temp_lsb = bus.read_byte (SHT21_ADD)
    #print temp_lsb
    temp_chksm = bus.read_byte (SHT21_ADD)
    #print temp_chksm
    
    temperature = (temp_msb << 8) + temp_lsb
    #print temperature
    temperature &= SHT21_STATUS_MASK
    #print temperature
    temperature *= 175.72
    #print temperature
    temperature /= 1<<16
    #print temperature
    temperature -= 46.85

    return temperature


def get_humidity():
    bus.write_byte(SHT21_ADD, SHT21_MEASURE_HUM_CMD)

    time.sleep(0.1)

    hum_msb = bus.read_byte (SHT21_ADD)
    #print temp_msb
    hum_lsb = bus.read_byte (SHT21_ADD)
    #print temp_lsb
    hum_chksm = bus.read_byte (SHT21_ADD)
    #print temp_chksm
    
    humidity = (hum_msb << 8) + hum_lsb
    #print temperature
    humidity &= SHT21_STATUS_MASK
    #print temperature
    humidity *= 125.0
    #print temperature
    humidity /= 1<<16
    #print temperature
    humidity -= 6

    return humidity




GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

steps = 20
micro_step = 1.0 / 4 #Possible values: 1.0, 1.0/2, 1.0/4, 1.0/8, 1.0/16, 1.0/32 

GPIO.setup(STEP_PIN, GPIO.OUT)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(NSLEEP_PIN, GPIO.OUT)
GPIO.setup(NFAULT_PIN, GPIO.IN)
GPIO.setup(NENBL_PIN, GPIO.OUT)
GPIO.setup(CONFIG_PIN, GPIO.OUT)


GPIO.output(NSLEEP_PIN, False)  #Low power and reset all logic
GPIO.output(CONFIG_PIN, True)   #Indexer mode
GPIO.output(NSLEEP_PIN, True)   #Enable device

time.sleep(0.001)

while GPIO.input(NFAULT_PIN)==0:
	time.sleep(0.001)

GPIO.output(NENBL_PIN, False) #Enable all outputs

if steps < 0:
	GPIO.output(DIR_PIN, False) #Anticlockwise
	steps = -steps             
else:
	GPIO.output(DIR_PIN, True)  #Clockwise

# Set the mode pins M0 and M1 to appropriate state 
# Setting a pin as input puts it in high impedance mode

if micro_step == 1:
    GPIO.setup(M1_PIN, GPIO.OUT)
    GPIO.output(M1_PIN, False)
    GPIO.setup(M0_PIN, GPIO.OUT)
    GPIO.output(M0_PIN, False)



try:
    while True:
        bus = smbus.SMBus(1)
        temperature = get_temperature()
        humidity = get_humidity()
        print "Temperature is ", temperature
        print "Humidity is ", humidity
	
        if (temperature > 40):
		    for count in np.arange(0, steps, micro_step):
			    time.sleep(0.05)
			    GPIO.output(STEP_PIN, True) # High going pulse moves the motor
			    time.sleep(0.05)
			    GPIO.output(STEP_PIN, False)
    
except:
    #print Error
    print "Error in executing I2C device program"
    

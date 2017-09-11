import RPi.GPIO as GPIO
import smbus
import time

SHT21_ADD = 0x40
SHT21_STATUS_MASK = 0xFFFC

SHT21_MEASURE_TEMP_CMD = 0xF3
SHT21_MEASURE_HUM_CMD = 0xF5

temperatureBarGraph = [27,21,18,12]
humidityBarGraph = [25,23,20,16]


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


for led_tmp in temperatureBarGraph:
    GPIO.setup(led_tmp, GPIO.OUT)

for led_hum in humidityBarGraph:
    GPIO.setup(led_hum, GPIO.OUT) 

for led_tmp in temperatureBarGraph:
    GPIO.output(led_tmp, GPIO.LOW) 

for led_hum in humidityBarGraph:
    GPIO.output(led_hum, GPIO.LOW)

#GPIO.output(16, GPIO.LOW)

try:
    bus = smbus.SMBus(1)

    print "Temperature is %s" % get_temperature()
    print "Humidity is %s" % get_humidity()
    
except:
    #print Error
    print "Error in executing I2C device program"


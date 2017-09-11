import RPi.GPIO as GPIO
import smbus
import time

SHT21_ADD = 0x40
SHT21_STATUS_MASK = 0xFFFC

SHT21_MEASURE_TEMP_CMD = 0xF3
SHT21_MEASURE_HUM_CMD = 0xF5

MAX_TEMPERATURE = 120
MAX_HUMIDITY = 100


temperatureBarGraph = [26,23,20,17,14,11,8,5]
humidityBarGraph = [27,24,21,18,15,12,9,6]
unusedLEDs = [16,13,10,7]

temperatureButton = 25
humidityButton = 22

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

for led_unused in unusedLEDs:
    GPIO.setup(led_unused, GPIO.OUT)
    GPIO.output(led_unused, GPIO.LOW)

GPIO.setup(temperatureButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(humidityButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)


temperatureLEDs = len(temperatureBarGraph)
humidityLEDs = len(humidityBarGraph)

temperatureDiv = int(MAX_TEMPERATURE / temperatureLEDs) - 1
humidityDiv = int(MAX_HUMIDITY / humidityLEDs)

try:
    bus = smbus.SMBus(1)
    while True:
        time.sleep(2)
        temperature = get_temperature()
        humidity = get_humidity()
        
        print "Temperature is ", temperature
        print "Humidity is ", humidity
        
        
        if (GPIO.input(temperatureButton)):
            bar_level = int(temperature/temperatureDiv)
            for led_temp in range(0, bar_level):
                #print led_temp
                GPIO.output(temperatureBarGraph[led_temp], GPIO.HIGH)
            for led_temp in range(bar_level, len(temperatureBarGraph)):
                GPIO.output(temperatureBarGraph[led_temp], GPIO.LOW)
        else:
            for led_tmp in temperatureBarGraph:
                GPIO.output(led_tmp, GPIO.LOW) 

        if (GPIO.input(humidityButton)):
            bar_level = int(humidity/humidityDiv)
            for led_temp in range(0, bar_level):
                #print led_temp
                GPIO.output(humidityBarGraph[led_temp], GPIO.HIGH)
            for led_temp in range(bar_level, len(humidityBarGraph)):
                GPIO.output(humidityBarGraph[led_temp], GPIO.LOW)
        else:
            for led_tmp in humidityBarGraph:
                GPIO.output(led_tmp, GPIO.LOW) 
            
except IOError as (errno, strerror):
    print "I/O error({0}): {1}. Try changing I2C device number in code".format(errno, strerror)
except KeyboardInterrupt:
    print "Keyboard Interrupt Received"
except:
    print "Unexpected error:"
    raise
finally:
    GPIO.cleanup()
    print "Exiting Program"

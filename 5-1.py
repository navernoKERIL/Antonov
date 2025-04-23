import RPi.GPIO as GPIO
import time

def decimal2binary(val):
    return [int(bit) for bit in bin(val)[2:].zfill(8)]


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
troyka = 13

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def adc():
    for i in range(256):
        dac_v = decimal2binary(i)
        GPIO.output(dac, dac_v)
        comp_v = GPIO.input(comp)
        time.sleep(0.01)
        if comp_v:
            return i
    return 0

try:
    while True:   
        x = adc()
        v = x*3.3/256
        if v: print(v, "V")
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
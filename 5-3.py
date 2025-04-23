import RPi.GPIO as GPIO
import time

def decimal2binary(val):
    return [int(bit) for bit in bin(val)[2:].zfill(8)]


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
troyka = 13
led = [9, 10, 22, 27, 17, 4, 3, 2]

GPIO.setup(led, GPIO.OUT)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def adc():
    k = 0
    for i in range (7, -1, -1):
        k += 2**i
        dac_v = decimal2binary(k)
        GPIO.output(dac, dac_v)
        time.sleep(0.01)     
        comp_v = GPIO.input(comp) 
        if comp_v:
            k -= 2**i
    return k 

def volume(val):
    val = int(val/32)
    arr = [0, 0, 0, 0, 0, 0, 0, 0]
    for i in range (val):
        arr[i] = 1
    return arr

try:
    while True:   
        x = adc()
        vol = volume(x)
        GPIO.output(led, vol)
        print (int(x/32))
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
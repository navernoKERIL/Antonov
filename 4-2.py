import RPi.GPIO as GPIO
import time

def decimal2binary(val):
    return [int(bit) for bit in bin(val)[2:].zfill(8)]


GPIO.setwarnings(False)
dac = [8, 11, 7, 1, 0, 5, 12, 6]
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

flag = 1
num = 0

try:
    period = float(input("enter period "))
    while True:   
        bin_t = decimal2binary(num)
        GPIO.output(dac, bin_t)
        print(num)
        if num == 0:
            flag = 1
        if num == 255:
            flag = 0
        if flag:
            num += 1
        else:
            num -= 1
        time.sleep(period/512)      
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
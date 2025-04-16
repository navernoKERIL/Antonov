import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.OUT)

p = GPIO.PWM(6, 1000)
p.start(0)

try:
    while True:
        x = int(input("enter number "))
        p.ChangeDutyCycle(x)
        print(x/100*33)
finally:
    GPIO.output(6, 0)
    GPIO.cleanup()
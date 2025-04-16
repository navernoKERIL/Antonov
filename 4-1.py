import RPi.GPIO as GPIO


def decimal2binary(val):
    return [int(bit) for bit in bin(val)[2:].zfill(8)]


GPIO.setwarnings(False)
dac = [8, 11, 7, 1, 0, 5, 12, 6]
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

try:
    while True:   
        num = input("enter a number in [0, 255) ")
        try:
            num = int(num)
            if 0 <= num <=255:
                GPIO.output(dac, decimal2binary(num))
                v = 3.3 * num / 256
                print(f"voltage is: {v:.4} V")
            else: 
                print("try a number in [0, 256) ")
        except Exception:
            if num == "q": break
            print("enter a number ")
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
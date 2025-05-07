import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import time

def dtb(value):
    return [int(i) for i in bin(value)[2:].zfill(8)]

dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
troyka = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.LOW)

def light_leds(value):
    dtb_val = dtb(value)
    GPIO.output(dac, dtb_val)
    return

def adc():
    level = 0
    for i in range (7, -1, -1):
        level += 2**i
        GPIO.output(dac, dtb(level))
        time.sleep(0.01)
        comp_val = GPIO.input(comp)
        if (comp_val == 0):
            level -= 2**i
    return level




data_volts = []
data_time = []

try:
    GPIO.output(troyka, GPIO.HIGH)
    t0 = time.time()
    value = 0
    while value < 256*0.97:
        value = adc()
        print(value/256*3.3)
        light_leds(value)
        data_volts.append(value)
        data_time.append(time.time() - t0)

    GPIO.output(troyka, GPIO.LOW)

    while value > 256*0.02:
        value = adc()
        print(value/256*3.3)
        light_leds(value)
        data_volts.append(value)
        data_time.append(time.time() - t0)


    t1 = time.time()
    with open("./settings.txt", "w") as file:
        file.write(str((t1 - t0) / len(data_volts)))
        file.write("\n")
        file.write(str(3.3/256))

finally: 
    GPIO.output(dac, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()

    data_volts_s = [str(item) for item in data_volts]
    data_time_s = [str(item) for item in data_time]

    with open("./data.txt", "w") as file:
        file.write("\n".join(data_volts_s))

    plt.plot(data_time, data_volts)
    plt.show()
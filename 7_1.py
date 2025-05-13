import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import time

# === Настройка GPIO ===
dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
troyka = 17
voltage = 3.3

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.LOW)

# === Функции ===
def dtb(value):
    return [int(i) for i in bin(value)[2:].zfill(8)]

def light_leds(value):
    GPIO.output(dac, dtb(value))

def adc():
    level = 0
    for i in range (7, -1, -1):
        level += 2**i
        light_leds(level)
        GPIO.output(dac, dtb(level))
        time.sleep(0.001)
        comp_val = GPIO.input(comp)
        if (comp_val == 0):
            level -= 2**i
    return level

# === Основной цикл ===
data_volts = []
data_adc = []
data_time = []

t0 = time.time()

try:
    # === Этап заряда ===
    print("Начало этапа заряда")
    GPIO.output(troyka, GPIO.HIGH)
    value = 0
    while value < 256*0.97:
        value = adc()
        voltage_current = value/256*3.3
        print("Заряд:", voltage_current, "В")
        light_leds(value)
        data_volts.append(voltage_current)
        data_adc.append(value)
        data_time.append(time.time() - t0)

    # === Этап разряда ===
    print("Начало этапа разряда")
    GPIO.output(troyka, GPIO.LOW)

    while value > 256*0.02:
        value = adc()
        voltage_current = value/256*3.3
        print("Разряд:", voltage_current, "В")
        light_leds(value)
        data_volts.append(voltage_current)
        data_adc.append(value)
        data_time.append(time.time() - t0)

    # === Обработка результатов ===
    t1 = time.time()
    experiment_duration = t1 - t0
    sampling_frequency = len(data_volts) / experiment_duration
    adc_step = voltage / 256

    # === Сохранение данных ===
    with open("./settings.txt", "w") as file:
        file.write(str(sampling_frequency))
        file.write("\n")
        file.write(str(adc_step))

    data_adc_s = [str(item) for item in data_adc]

    with open("./data.txt", "w") as file:
        file.write("\n".join(data_adc_s))

    # === Вывод графика ===
    plt.plot(data_time, data_volts)
    plt.xlabel("Время (с)")
    plt.ylabel("Напряжение (В)")
    plt.title("Процесс заряда и разряда конденсатора")
    plt.show()

    # === Вывод в терминал ===
    print("Период измерения:", experiment_duration / len(data_volts), "с")
    print("Частота дискретизации:", sampling_frequency, "Гц")
    print("Шаг квантования АЦП:", adc_step, "В")

finally:
    # === Завершение ===
    GPIO.output(dac, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()
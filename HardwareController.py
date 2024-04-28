import RPi.GPIO as GPIO
from threading import Thread
import time

from RpiMotorLib import RpiMotorLib

BLUE_LED_PIN   = 17
YELLOW_LED_PIN = 27
RED_LED_PIN    = 22
BUZZER_PIN     = 4
MOTOR_PINS = [19, 26, 21, 13]

BUZZER_NOTE_C = 262
BUZZER_NOTE_D = 294
BUZZER_NOTE_E = 330
BUZZER_NOTE_F = 349
BUZZER_NOTE_G = 392
BUZZER_NOTE_A = 440
BUZZER_NOTE_B = 494

BUZZER_DURATION_SHORT = 0.2
BUZZER_DURATION_LONG = 0.4


class HardwareController:
    rpi_motor: RpiMotorLib.BYJMotor = None
    buzzer: GPIO.PWM
    melody: list = [
        (BUZZER_NOTE_C, BUZZER_DURATION_SHORT),
        (BUZZER_NOTE_D, BUZZER_DURATION_SHORT),
        (BUZZER_NOTE_E, BUZZER_DURATION_SHORT),
        (BUZZER_NOTE_F, BUZZER_DURATION_SHORT),
        (BUZZER_NOTE_G, BUZZER_DURATION_SHORT),
        (BUZZER_NOTE_A, BUZZER_DURATION_SHORT),
        (BUZZER_NOTE_B, BUZZER_DURATION_SHORT),
        (BUZZER_NOTE_C, BUZZER_DURATION_LONG)
    ]

    def __init__(self):
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(BLUE_LED_PIN, GPIO.OUT)
        GPIO.setup(YELLOW_LED_PIN, GPIO.OUT)
        GPIO.setup(RED_LED_PIN, GPIO.OUT)
        GPIO.setup(BUZZER_PIN, GPIO.OUT)

        self.rpi_motor = RpiMotorLib.BYJMotor("MyMotorName", "28BYJ")

        self.buzzer = GPIO.PWM(BUZZER_PIN, BUZZER_NOTE_C)

    def turnMotor(self, speed=0.001, angle_degs=45, ccwise=False):
        t = Thread(target=self.__turnMotor, args=(speed, angle_degs, ccwise))
        t.start()
    def __turnMotor(self, speed, angle_degs, ccwise):
        self.rpi_motor.motor_run(MOTOR_PINS, speed, 512*angle_degs/360, ccwise, False, "half", 0.05)
    
    def dispenseFood(self, units=1):
        t = Thread(target=self.__dispenseFood, args=(units,))
        t.start()
    def __dispenseFood(self, units):
        self.__turnMotor(0.001, 45*units, False)

    def playMelody(self):
        t = Thread(target=self.__playMelody)
        t.start()
    def __playMelody(self):
        self.buzzer.start(50)
        for note, duration in self.melody:
                self.buzzer.ChangeFrequency(note)
                time.sleep(duration)
        self.buzzer.stop()

    def displayBinLED(self, num: int):
        t = Thread(target=self.__displayBinLED, args=(num,))
        t.start()
    def __displayBinLED(self, num):
        if num % 8 != num % 4: GPIO.output(BLUE_LED_PIN, GPIO.HIGH)
        if num % 4 != num % 2: GPIO.output(YELLOW_LED_PIN, GPIO.HIGH)
        if num % 2 != 0      : GPIO.output(RED_LED_PIN, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(BLUE_LED_PIN, GPIO.LOW)
        GPIO.output(YELLOW_LED_PIN, GPIO.LOW)
        GPIO.output(RED_LED_PIN, GPIO.LOW)
    
    def setLED(self, id, hot=True):
        t = Thread(target=self.__setLED, args=(id, hot))
        t.start()
    def __setLED(self, id, hot):
        signal = GPIO.LOW
        if hot: signal = GPIO.HIGH
        if   id % 3 == 1: GPIO.output(BLUE_LED_PIN, signal)
        elif id % 3 == 2: GPIO.output(YELLOW_LED_PIN, signal)
        elif id % 3 == 0: GPIO.output(RED_LED_PIN, signal)
    
    def resetLEDs(self):
        t = Thread(target=self.__resetLEDs)
        t.start()
    def __resetLEDs(self):
        self.__setLED(1, False)
        self.__setLED(2, False)
        self.__setLED(3, False)



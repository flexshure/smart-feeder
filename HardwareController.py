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

    def turn_motor(self, speed=0.001, angle_degs=45, ccwise=False):
        t = Thread(target=self.__turn_motor, args=(speed, angle_degs, ccwise))
        t.start()
    def __turn_motor(self, speed, angle_degs, ccwise):
        self.rpi_motor.motor_run(MOTOR_PINS, speed, 512*angle_degs/360, ccwise, False, "half", 0.05)
    
    def dispense_food(self, units=1):
        t = Thread(target=self.__dispense_food, args=(units,))
        t.start()
    def __dispense_food(self, units):
        self.__turn_motor(0.001, 45*units, False)

    def play_melody(self):
        t = Thread(target=self.__play_melody)
        t.start()
    def __play_melody(self):
        self.buzzer.start(50)
        for note, duration in self.melody:
                self.buzzer.ChangeFrequency(note)
                time.sleep(duration)
        self.buzzer.stop()

    def display_bin_LED(self, num: int):
        t = Thread(target=self.__display_bin_LED, args=(num,))
        t.start()
    def __display_bin_LED(self, num):
        if num % 8 != num % 4: GPIO.output(BLUE_LED_PIN, GPIO.HIGH)
        if num % 4 != num % 2: GPIO.output(YELLOW_LED_PIN, GPIO.HIGH)
        if num % 2 != 0      : GPIO.output(RED_LED_PIN, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(BLUE_LED_PIN, GPIO.LOW)
        GPIO.output(YELLOW_LED_PIN, GPIO.LOW)
        GPIO.output(RED_LED_PIN, GPIO.LOW)
    
    def set_LED(self, id, hot=True):
        t = Thread(target=self.__set_LED, args=(id, hot))
        t.start()

    def __set_LED(self, id, hot):
        signal = GPIO.LOW
        if hot: signal = GPIO.HIGH
        if   id % 3 == 1: GPIO.output(BLUE_LED_PIN, signal)
        elif id % 3 == 2: GPIO.output(YELLOW_LED_PIN, signal)
        elif id % 3 == 0: GPIO.output(RED_LED_PIN, signal)
    
    def reset_LEDs(self):
        t = Thread(target=self.__reset_LEDs)
        t.start()
    def __reset_LEDs(self):
        self.__set_LED(1, False)
        self.__set_LED(2, False)
        self.__set_LED(3, False)

    def blink_LED(self, id, hot=True, num_blinks):
        pass

import RPi.GPIO as GPIO

from enum import Enum
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

class LED(Enum):
    BLUE = 1
    YELLOW = 2
    RED = 3

class HardwareController:
    rpi_motor: RpiMotorLib.BYJMotor = None

    __blue_led_status   = False
    __yellow_led_status = False
    __red_led_status    = False

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
        if GPIO.getmode() is None:
            GPIO.setmode(GPIO.BCM)
        
        GPIO.setup(BLUE_LED_PIN, GPIO.OUT)
        GPIO.setup(YELLOW_LED_PIN, GPIO.OUT)
        GPIO.setup(RED_LED_PIN, GPIO.OUT)
        GPIO.setup(BUZZER_PIN, GPIO.OUT)

        self.reset_LEDs()

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
        if num % 8 != num % 4: self.__set_LED(LED.BLUE, GPIO.LOW)
        if num % 4 != num % 2: self.__set_LED(LED.YELLOW, GPIO.LOW)
        if num % 2 != 0      : self.__set_LED(LED.RED, GPIO.LOW)
        time.sleep(1)
        self.__set_LED(LED.BLUE, GPIO.LOW)
        self.__set_LED(LED.YELLOW, GPIO.LOW)
        self.__set_LED(LED.RED, GPIO.LOW)
    
    def blink_LED_from_id(self, id: int, num_blinks: int=1):
        t = Thread(target=self.__blink_LED_from_id, args=(id, num_blinks))
        t.start()
    def __blink_LED_from_id(self, id, num_blinks):
        if   id % 3 == 1: self.__blink_LED(LED.BLUE, num_blinks)
        elif id % 3 == 2: self.__blink_LED(LED.YELLOW, num_blinks)
        else:             self.__blink_LED(LED.RED, num_blinks)
    
    def blink_LED(self, led: LED, num_blinks: int=1):
        t = Thread(target=self.__blink_LED, args=(led, num_blinks,))
        t.start()
    def __blink_LED(self, led, num_blinks):
        hot = self.get_LED(led)
        for i in range(num_blinks):
            signal = GPIO.HIGH
            if hot: signal = GPIO.LOW
            if   led == LED.BLUE:   GPIO.output(BLUE_LED_PIN, signal)
            elif led == LED.YELLOW: GPIO.output(YELLOW_LED_PIN, signal)
            elif led == LED.RED:    GPIO.output(RED_LED_PIN, signal)
            time.sleep(0.5)
            signal = GPIO.LOW
            if hot: signal = GPIO.HIGH
            if   led == LED.BLUE:   GPIO.output(BLUE_LED_PIN, signal)
            elif led == LED.YELLOW: GPIO.output(YELLOW_LED_PIN, signal)
            elif led == LED.RED:    GPIO.output(RED_LED_PIN, signal)
            time.sleep(0.5)
    
    def set_LED_from_id(self, id, hot=True):
        t = Thread(target=self.__set_LED_from_id, args=(id, hot))
        t.start()
    def __set_LED_from_id(self, id, hot):
        if   id % 3 == 1: self.__set_LED(LED.BLUE, hot)
        elif id % 3 == 2: self.__set_LED(LED.YELLOW, hot)
        else:             self.__set_LED(LED.RED, hot)
    
    def get_LED(self, led: LED):
        if   led == LED.BLUE:   return self.__blue_led_status
        elif led == LED.YELLOW: return self.__yellow_led_status
        elif led == LED.RED:    return self.__red_led_status

    def set_LED(self, led: LED, on=True):
        t = Thread(target=self.__set_LED, args=(id, led))
        t.start()
    def __set_LED(self, led, hot):
        signal = GPIO.LOW
        if hot: signal = GPIO.HIGH
        if led == LED.BLUE:
            GPIO.output(BLUE_LED_PIN, signal)
            self.__blue_led_status = hot
        elif led == LED.YELLOW:
            GPIO.output(YELLOW_LED_PIN, signal)
            self.__yellow_led_status = hot
        elif led == LED.RED:
            GPIO.output(RED_LED_PIN, signal)
            self.__red_led_status = hot
    
    def reset_LEDs(self):
        t = Thread(target=self.__reset_LEDs)
        t.start()
    def __reset_LEDs(self):
        self.__set_LED(LED.BLUE, False)
        self.__set_LED(LED.YELLOW, False)
        self.__set_LED(LED.RED, False)



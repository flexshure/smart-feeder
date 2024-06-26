from mfrc522 import SimpleMFRC522
from datetime import datetime, timezone

import schedule
from Time import Time
import time
from threading import Thread
from Kintone import Kintone
from HardwareController import HardwareController

def midnight_reset():
    controller.reset_LEDs()
    for pet_id in server.last_eaten_table:
        server.push_last_eaten_timestamp(entry, "")

def main():
    controller = HardwareController()
    reader = SimpleMFRC522()
    server = Kintone()

    schedule.every().day.at("00:00:00").do(midnight_reset)
    def __schedule_loop():
        while True:
            time.sleep(1)
            schedule.run_pending()
    t = Thread(target=__schedule_loop)
    t.start()

    ''' TODO:
    -Buzzer
        .interrupt 15 minutes after each scheduled meal, `chime' if pet hasn't eaten

    '''
    while True:
        # blocking read
        last_read_nfc = reader.read_id()

        pet_id = server.pet_id_from_NFC(str(last_read_nfc))

        last_eaten = server.get_last_eaten_timestamp(str(pet_id)) # -> Time
        mealtimes = server.get_mealtimes(str(pet_id)) # list of Time

        now = Time(hours=datetime.now().hour, minutes=datetime.now().minute)

        # count how many mealtimes between last_eaten_mealtime and now
        # populates meal_credit
        meal_credit = 0
        for scheduled_time in mealtimes:
            if last_eaten >= scheduled_time:
                continue

            if now >= scheduled_time:
                meal_credit += 1 

        if meal_credit == 0:
            # nothing to dispense, continue to next tag scan
            # blink LED
            controller.blink_LED_from_id(int(pet_id), num_blinks=3)
            continue

        units_to_dispense = meal_credit * int(server.schedule_table[pet_id]['units_food'])

        controller.dispense_food(units_to_dispense)
        # display on LED which pet got dispensed to

        if now > mealtimes[-1]:
            # pet has eaten all meals for today
            controller.set_LED_from_id(int(pet_id))

        server.push_last_eaten_timestamp(pet_id, now)

        time.sleep(5)

if __name__ == "__main__":
    main()
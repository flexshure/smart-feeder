import nfc
from gpiozero import LED
from mfrc522 import SimpleMFRC522
from datetime import datetime, timezone

from Time import Time
from Kintone import Kintone
from HardwareController import HardwareController

# def time0_is_after_time1(time_0, time_1):
#     if time_0[HOUR] > time_1[HOUR]:
#         return True
#     elif time_0[HOUR] == time_1[HOUR]:
#         if time_0[MINUTE] >= time_1[MINUTE]:
#             return True

#     return False



def main():
    reader = SimpleMFRC522()
    server = Kintone()
    controller = HardwareController()

    while True:
        # blocking read
        last_read_nfc = reader.read_id()

        server.update_schedule()
        pet_id = server.pet_id_from_NFC(last_read_nfc)

        last_eaten = server.get_last_eaten_timestamp(pet_id) # -> Time

        mealtimes = server.get_mealtimes(pet_id) # list of Time

        now = Time(hours=datetime.now().hour, minutes=datetime.now().minute)

        meal_credit = 0

        # count how many mealtimes between last_eaten_mealtime and now
        # populates meal_credit
        for scheduled_time in mealtimes:
            if last_eaten >= scheduled_time:
                continue

            if now >= scheduled_time:
                meal_credit += 1 

        if now > mealtimes[-1] and meal_credit == 0:
            # pet has eaten all meals for today
            controller.set_led(pet_id)

        if meal_credit == 0:
            # continue to next tag scan
            continue

        units_to_dispense = meal_credit * server.schedule_table[pet_id]['UnitsFood']

        controller.dispense_units(units_to_dispense) # display on LED which pet got dispensed to

        server.push_last_eaten_timestamp(pet_id, now)


        '''
        Main loop structure:
        
        check NFC sensor
            --> if tag detected, refresh data from kintone
                match NFC tag detected to a pet
                
                check if pet is able to eat (check set times for pet's meals and last time pet has eaten)
                    If able to eat --> dispense food (use given pet's units of food to rotate motor a certain number of degrees)
                    If not able to eat --> (maybe play sound)

            
            Potential ideas / stretch goals : 
                - If pet hasn't eaten 10 minutes past scheduled meal, play a sound or song
        '''
    pass

if __name__ == "__main__":
    main()
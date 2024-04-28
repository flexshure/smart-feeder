import nfc
from gpiozero import LED
from mfrc522 import SimpleMFRC522

import threading

reader = SimpleMFRC522()

def main():
    while True:

        # blocking read
        last_read_id = reader.read_id()


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
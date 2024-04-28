import RPi.GPIO as GPIO
import MFRC522

reader = MFRC522.MFRC522()

def read_data(sector):
    status = reader.MFRC522_Auth(reader.PICC_AUTHENT1A, sector, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], reader.uid)
    if status == reader.MI_OK:
        data = reader.MFRC522_Read(sector)
        return data
    else:
        return None

sector_to_read = 1
read_data = read_data(sector_to_read)
if read_data is not None:
    print("Data read:", read_data)
else:
    print("Error reading data")

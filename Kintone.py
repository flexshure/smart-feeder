import requests
import json
from Time import Time

class Kintone:
    schedule_table = {}

    def update_schedule(self):
        id = 1
        while True:
            url = 'https://nfc-smart-feeder.kintone.com/k/v1/record.json?app=1&id=' + str(id)
            response = requests.get(url, headers={'X-Cybozu-API-Token': 'CvLah6cYe2KZgVxbKeAgjVERCcnMSDbXjd3Hrab5'})
            if "is not found" in response.text:
                break
            
            response = json.loads(response.text)
            #parse response
            name = response["record"]["Text"]["value"]
            meal_times = response["record"]["Text_0"]["value"]
            meal_times = meal_times.split(',')
            quantity_food = response["record"]["Number"]["value"]
            nfc_tag = response["record"]["Text_1"]["value"]
            food_type = response["record"]["Text_2"]["value"]
            pet_id = response["record"]["Record_number"]["value"]
            #store data in dictionary
            self.schedule_table[pet_id] = {"name": name, "units_food": quantity_food, "meal_times": meal_times, "NFC_ID": nfc_tag, "food_type": food_type}
            id = id + 1

    def get_last_eaten_timestamp(self, pet_id):
        id = 1
        while True:
            url = "https://nfc-smart-feeder.kintone.com/k/v1/record.json?app=2&id=" + str(id)
            response = requests.get(url, headers={'X-Cybozu-API-Token': 'RKylBI2WhrLWJoSba87HT3b5QgBuuWIh6xF1Plyc'})
            
            if "is not found" in response.text:
                break
            response = json.loads(response.text)
            if pet_id == response["record"]["Text_0"]["value"]:
                if response["record"]["Text_1"]["value"] == "":
                    return Time(0, 0)
                split = response["record"]["Text_1"]["value"].split(":")
                return Time(split[0], split[1])
            id = id + 1

    def pet_id_from_NFC(self, NFC_ID):
        for entry in self.schedule_table:
            if self.schedule_table[entry]["NFC_ID"] == NFC_ID:
                print(entry)
                return entry
            
        return self.update_pet_NFC_ID(NFC_ID)

    def add_empty_entry_last_eaten_app(self, pet_ID, pet_name):
        api_url = "https://nfc-smart-feeder.kintone.com/k/v1/record.json"
        #send a new data record, ISSUE: Can't set Record_number (aka pet_id)
        postJson = {'app': 2,'record': {'Text': {'value': pet_name},'Text_1': {'value': 'NULL'}}}
        post = requests.post(api_url, headers={'X-Cybozu-API-Token': 'RKylBI2WhrLWJoSba87HT3b5QgBuuWIh6xF1Plyc'}, json=postJson)

    def update_pet_NFC_ID(self, NFC_ID):
        for entry in self.schedule_table:
            if self.schedule_table[entry]["NFC_ID"] == "":
                self.schedule_table[entry]["NFC_ID"] = NFC_ID
                self.push_updated_NFC_to_db(entry, NFC_ID)
                #self.add_empty_entry_last_eaten_app(entry, self.schedule_table[entry]["Name"])
                return entry

    def push_updated_NFC_to_db(self, pet_id, NFC_ID):
        url = "https://nfc-smart-feeder.kintone.com/k/v1/record.json?app=1&id=" + str(pet_id)
        postJson = {'app': 1,'id': pet_id,'record': {'Text_1': {'value': NFC_ID}}}
        post = requests.put(url, headers={'X-Cybozu-API-Token': 'CvLah6cYe2KZgVxbKeAgjVERCcnMSDbXjd3Hrab5'}, json=postJson)
    
    def push_last_eaten_timestamp(self, pet_id, now):
        url = "https://nfc-smart-feeder.kintone.com/k/v1/record.json?app=2&id=" + str(pet_id)
        postJson = {'app': 2,'id': pet_id,'record': {'Text_1': {'value': now}}}
        post = requests.put(url, headers={'X-Cybozu-API-Token': 'RKylBI2WhrLWJoSba87HT3b5QgBuuWIh6xF1Plyc'}, json=postJson)
    
    def get_mealtimes(self, pet_id):
        meal_times = self.schedule_table[str(pet_id)]["meal_times"]
        meal_times_formatted = []
        for i in range(0, len(meal_times)):
            split = meal_times[i].split(':')
            my_time = Time(hours=int(split[0]), minutes=int(split[1]))
            meal_times_formatted.append(my_time)
        return meal_times_formatted
    
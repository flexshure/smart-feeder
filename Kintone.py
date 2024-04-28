import requests
import json
from Time import Time

class Kintone:
    schedule_table = {}
    last_eaten_table = {}

    def update_schedule(self):
        url = 'https://nfc-smart-feeder.kintone.com/k/v1/records.json?app=1'
        response = requests.get(url, headers={'X-Cybozu-API-Token': 'CvLah6cYe2KZgVxbKeAgjVERCcnMSDbXjd3Hrab5'})
            
        response = json.loads(response.text)
        
        for i in range(0, len(response["records"])): 
            name = response["records"][i]["Text"]["value"]
            meal_times = response["records"][i]["Text_0"]["value"]
            meal_times = meal_times.split(',')
            quantity_food = response["records"][i]["Number"]["value"]
            nfc_tag = response["records"][i]["Text_1"]["value"]
            food_type = response["records"][i]["Text_2"]["value"]
            pet_id = response["records"][i]["Record_number"]["value"]
            #store data in dictionary
            self.schedule_table[pet_id] = {"name": name, "units_food": quantity_food, "meal_times": meal_times, "NFC_ID": nfc_tag, "food_type": food_type}

    def update_last_eaten(self):
        id = 1
        url = 'https://nfc-smart-feeder.kintone.com/k/v1/records.json?app=2'
        response = requests.get(url, headers={'X-Cybozu-API-Token': 'RKylBI2WhrLWJoSba87HT3b5QgBuuWIh6xF1Plyc'})
        
        response = json.loads(response.text)

        for i in range(0, len(response["records"])):
            pet_id = response["records"][i]["Text_0"]["value"]

            if response["records"][i]["Text_1"]["value"] == "":
                last_ate = Time(0,0)
            else:
                time = response["records"][i]["Text_1"]["value"].split(":")
                last_ate = Time(int(time[0]), int(time[1]))
            name = response["records"][i]["Text"]["value"]
            record_number = response["records"][i]["Record_number"]["value"]
                
            self.last_eaten_table[pet_id] = {"name": name, "last_ate": last_ate, "record_number": record_number}

    def get_last_eaten_timestamp(self, pet_id):
        self.update_last_eaten()
        return self.last_eaten_table[pet_id]["last_ate"]

    def pet_id_from_NFC(self, NFC_ID):
        self.update_schedule()
        for entry in self.schedule_table:
            if self.schedule_table[entry]["NFC_ID"] == NFC_ID:
                return entry
            
        return self.update_pet_NFC_ID(NFC_ID)

    def add_empty_entry_last_eaten(self, pet_ID, pet_name):
        api_url = "https://nfc-smart-feeder.kintone.com/k/v1/record.json"
        #send a new data record, ISSUE: Can't set Record_number (aka pet_id)
        postJson = {'app': 2,'record': {'Text': {'value': pet_name},'Text_1': {'value': ''}, 'Text_0': {'value': pet_ID}}}
        post = requests.post(api_url, headers={'X-Cybozu-API-Token': 'RKylBI2WhrLWJoSba87HT3b5QgBuuWIh6xF1Plyc'}, json=postJson)

    def update_pet_NFC_ID(self, NFC_ID):
        self.update_last_eaten()
        for entry in self.schedule_table:
            if self.schedule_table[entry]["NFC_ID"] == "":
                self.schedule_table[entry]["NFC_ID"] = NFC_ID
                self.push_updated_NFC_to_db(entry, NFC_ID)

                if entry not in self.last_eaten_table.keys():
                    print(f"adding new row for {entry} ({type(entry)})")
                    print(f"keys: {self.last_eaten_table.keys()}")

                    self.add_empty_entry_last_eaten(entry, self.schedule_table[entry]["name"])

                return entry

    def push_updated_NFC_to_db(self, pet_id, NFC_ID):
        url = "https://nfc-smart-feeder.kintone.com/k/v1/record.json?app=1&id=" + str(pet_id)
        postJson = {'app': 1,'id': pet_id,'record': {'Text_1': {'value': NFC_ID}}}
        post = requests.put(url, headers={'X-Cybozu-API-Token': 'CvLah6cYe2KZgVxbKeAgjVERCcnMSDbXjd3Hrab5'}, json=postJson)
    
    def push_last_eaten_timestamp(self, pet_id, now):
        #reset case at midnight
        if type(now) == str and now == "":
            record_number = str(self.get_record_number_from_pet_id(pet_id))
            url = "https://nfc-smart-feeder.kintone.com/k/v1/record.json?app=2&id=" + record_number
            postJson = {'app': 2,'id': record_number,'record': {'Text_1': {'value': ""}}}
            post = requests.put(url, headers={'X-Cybozu-API-Token': 'RKylBI2WhrLWJoSba87HT3b5QgBuuWIh6xF1Plyc'}, json=postJson)
            return

        record_number = str(self.get_record_number_from_pet_id(pet_id))
        url = "https://nfc-smart-feeder.kintone.com/k/v1/record.json?app=2&id=" + record_number

        if(now.minutes <= 9):
            time = str(now.hours) + ":0" + str(now.minutes)
        else:   
            time = str(now.hours) + ":" + str(now.minutes)
        postJson = {'app': 2,'id': record_number,'record': {'Text_1': {'value': time}}}
        post = requests.put(url, headers={'X-Cybozu-API-Token': 'RKylBI2WhrLWJoSba87HT3b5QgBuuWIh6xF1Plyc'}, json=postJson)

    def get_record_number_from_pet_id(self, pet_id):
        self.update_last_eaten()
        return self.last_eaten_table[pet_id]["record_number"]
        '''
        while True:
            url = "https://nfc-smart-feeder.kintone.com/k/v1/record.json?app=2&id=" + str(id)
            response = requests.get(url, headers={'X-Cybozu-API-Token': 'RKylBI2WhrLWJoSba87HT3b5QgBuuWIh6xF1Plyc'})
            
            if "is not found" in response.text:
                break

            response = json.loads(response.text)
            if response["record"]["Text_0"]["value"] == pet_id:
                return response["record"]["Record_number"]["value"]

            id = id + 1
        '''
    
    def get_mealtimes(self, pet_id):
        self.update_last_eaten()
        meal_times = self.schedule_table[str(pet_id)]["meal_times"]
        meal_times_formatted = []
        for i in range(0, len(meal_times)):
            split = meal_times[i].split(':')
            my_time = Time(hours=int(split[0]), minutes=int(split[1]))
            meal_times_formatted.append(my_time)
        return meal_times_formatted
    
import requests
import json

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
            mealTimes = response["record"]["Text_0"]["value"]
            mealTimes = mealTimes.split(',')
            quantityFood = response["record"]["Number"]["value"]
            nfcTag = response["record"]["Text_1"]["value"]
            foodType = response["record"]["Text_2"]["value"]
            petID = response["record"]["Record_number"]["value"]
            #store data in dictionary
            self.schedule_table[petID] = {"Name": name, "UnitsFood": quantityFood, "MealTimes": mealTimes, "NFC_ID": nfcTag, "FoodType": foodType}
            id = id + 1

    def get_last_eaten_timestamp(self, petID):
        id = 1
        while True:
            url = "https://nfc-smart-feeder.kintone.com/k/v1/record.json?app=2&id=" + str(id)
            response = requests.get(url, headers={'X-Cybozu-API-Token': 'RKylBI2WhrLWJoSba87HT3b5QgBuuWIh6xF1Plyc'})
            
            if "is not found" in response.text:
                break
            response = json.loads(response.text)
            if petID == response["record"]["$id"]["value"]:
                #convert time representations
                return response["record"]["Text_1"]["value"]  
            id = id + 1

    def pet_id_from_NFC(self, NFC_ID):
        for entry in self.schedule_table:
            if self.schedule_table[entry]["NFC_ID"] == NFC_ID:
                print(entry)
                return entry
            
        return self.update_pet_NFC_ID(NFC_ID)
        #add null entry to app2

    def add_empty_entry_last_eaten_app(self, pet_ID, pet_name):
        api_url = "https://nfc-smart-feeder.kintone.com/k/v1/record.json"
        #send a new data record, ISSUE: Can't set Record_number (aka petID)
        postJson = {'app': 2,'record': {'Text': {'value': pet_name},'Text_1': {'value': 'NULL'}}}
        post = requests.post(api_url, headers={'X-Cybozu-API-Token': 'RKylBI2WhrLWJoSba87HT3b5QgBuuWIh6xF1Plyc'}, json=postJson)

    def update_pet_NFC_ID(self, NFC_ID):
        for entry in self.schedule_table:
            if self.schedule_table[entry]["NFC_ID"] == "":
                self.schedule_table[entry]["NFC_ID"] = NFC_ID
                self.push_updated_NFC_to_db(entry, NFC_ID)
                #self.add_empty_entry_last_eaten_app(entry, self.schedule_table[entry]["Name"])
                return entry

    def push_updated_NFC_to_db(self, petID, NFC_ID):
        url = "https://nfc-smart-feeder.kintone.com/k/v1/record.json?app=1&id=" + str(petID)
        postJson = {'app': 1,'id': petID,'record': {'Text_1': {'value': NFC_ID}}}
        post = requests.put(url, headers={'X-Cybozu-API-Token': 'CvLah6cYe2KZgVxbKeAgjVERCcnMSDbXjd3Hrab5'}, json=postJson)
    
    def push_last_eaten_timestamp(self, petID, now):
        url = "https://nfc-smart-feeder.kintone.com/k/v1/record.json?app=2&id=" + str(petID)
        postJson = {'app': 2,'id': petID,'record': {'Text_1': {'value': now}}}
        post = requests.put(url, headers={'X-Cybozu-API-Token': 'RKylBI2WhrLWJoSba87HT3b5QgBuuWIh6xF1Plyc'}, json=postJson)
    
    '''
    def updateLastTimeEaten(petName, lastTimeEaten):
        for i in range(0, len(petData)):
            
            api_url = "https://nfc-smart-feeder.kintone.com/k/v1/record.json?app=2&id=1"
            #send a new data record
            postJson = {'app': 2,'record': {'Text': {'value': petName},'Text_1': {'value': lastTimeEaten}}}
            post = requests.post(api_url, headers={'X-Cybozu-API-Token': 'RKylBI2WhrLWJoSba87HT3b5QgBuuWIh6xF1Plyc'}, json=postJson)

        #update a data record
        postJson = {'app': 2,'id': 1,'record': {'Text': {'value': 'YEEE'},'Text_1': {'value': 'April 27, 6:52 PM'}}}
        post = requests.put(api_url, headers={'X-Cybozu-API-Token': 'RKylBI2WhrLWJoSba87HT3b5QgBuuWIh6xF1Plyc'}, json=postJson)
    '''
    
import requests
import json

class Kintone:
    petData = {}
    lastEatenData = {}

    def refreshPetData(self):
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
            petID = response["record"]["$id"]["value"]
            #store data in dictionary
            self.petData[petID] = {"Name": name, "UnitsFood": quantityFood, "MealTimes": mealTimes, "NFC Tag": nfcTag, "FoodType": foodType}
            id = id + 1
        
        return self.petData

    def refreshTimeLastEatenData(self):
        id = 1
        while True:
            url = "https://nfc-smart-feeder.kintone.com/k/v1/record.json?app=2&id=" + str(id)
            response = requests.get(url, headers={'X-Cybozu-API-Token': 'RKylBI2WhrLWJoSba87HT3b5QgBuuWIh6xF1Plyc'})
            
            if "is not found" in response.text:
                break
            
            response = json.loads(response.text)

            name = response["record"]["Text"]["value"]
            self.lastEatenData[name] = response["record"]["Text_1"]["value"]

            id = id + 1
            
        return self.lastEatenData

    def getTimeLastEaten(self, petName):
        id = 1
        while True:
            url = "https://nfc-smart-feeder.kintone.com/k/v1/record.json?app=2&id=" + str(id)
            response = requests.get(url, headers={'X-Cybozu-API-Token': 'RKylBI2WhrLWJoSba87HT3b5QgBuuWIh6xF1Plyc'})
            
            if "is not found" in response.text:
                break
            
            response = json.loads(response.text)

            if petName == response["record"]["Text"]["value"]:
                return response["record"]["Text_1"]["value"]
          
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
    
import requests
import json

#Get and parse all data from Kintone about individual pet's needs
id = 1
data = {}
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
    #store data in dictionary
    data[name] = {"UnitsFood": quantityFood, "MealTimes": mealTimes, "NFC Tag": nfcTag, "FoodType": foodType}
    id = id + 1


print(data)
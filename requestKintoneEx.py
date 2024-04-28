import requests
import json

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
    timeBtwnMeals = response["record"]["Number_0"]["value"]
    quantityFood = response["record"]["Number"]["value"]
   
    #store data in dictionary
    data[name] = {"UnitsFood": quantityFood, "TimeBtwnMeals": timeBtwnMeals}
    id = id + 1

print(data)
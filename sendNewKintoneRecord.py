import requests
api_url = "https://nfc-smart-feeder.kintone.com/k/v1/record.json?app=2&id=1"
#send a new data record
postJson = {'app': 2,'record': {'Text': {'value': 'Neem'},'Text_1': {'value': 'April 27, 6:12 PM'}}}
print(postJson)
post = requests.post(api_url, headers={'X-Cybozu-API-Token': 'RKylBI2WhrLWJoSba87HT3b5QgBuuWIh6xF1Plyc'}, json=postJson)

print(response)

#update a data record
postJson = {'app': 2,'id': 1,'record': {'Text': {'value': 'YEEE'},'Text_1': {'value': 'April 27, 6:52 PM'}}}
post = requests.put(api_url, headers={'X-Cybozu-API-Token': 'RKylBI2WhrLWJoSba87HT3b5QgBuuWIh6xF1Plyc'}, json=postJson)

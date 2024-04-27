import requests
response = requests.get('https://nfc-smart-feeder.kintone.com/k/v1/record.json?app=1&id=1', headers={'X-Cybozu-API-Token': 'CvLah6cYe2KZgVxbKeAgjVERCcnMSDbXjd3Hrab5'})

print(response.json)
print(response.text)

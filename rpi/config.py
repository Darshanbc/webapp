import json

with open("config.json") as json_file:
    json_data = json.load(json_file)
    
access_key=str(json_data['access_key'])
access_key_id=str(json_data['access_key_id'])
region=str(json_data['region'])
bucketName=str(json_data['bucketName'])
print bucketName
#print region



import json
import sys
import requests
r = requests.get('http://api.thingspeak.com/channels/659292/feeds.json?results=2')
data=r

json_str = json.dumps(data)

#//load the json to a string
resp = json.loads(json_str)

#//print the resp
print (resp)

#//extract an element in the response
print (resp['field1'])
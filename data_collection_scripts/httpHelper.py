import json
from time import sleep
import requests
import secrets

requestsMade = 0

def makeGetRequest(url):
    global requestsMade
    global keyNum
    if requestsMade % 30 == 0 and requestsMade !=0 :
        print ('Made 10 requests, sleeping for 10 seconds')
        sleep(10)

    print ('Get request for: ' + url)
    params = dict(
        api_key= secrets.getRiotAPIKey()
    )
    resp = requests.get(url=url, params=params)

    if resp.status_code==404:
        print ('404 - Skipping.')
        return None
    
    if resp.status_code==429:
        print ('Too many requests, pausing.')
        sleep(15)
        resp = requests.get(url=url, params=params)

    # while resp.status_code == 429:
        # print ('Too many requests, pausing.')
        # sleep(10)
        # resp = requests.get(url=url, params=params)

    # while resp.status_code != 200:
        # print resp.status_code
        # print ('Rito pls')
        # sleep(10)
        # resp = requests.get(url=url, params=params)

    requestsMade += 1
    print ('Requests made: ' + str(requestsMade))
    return json.loads(resp.text)

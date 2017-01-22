import mysql.connector
import secrets
import json
import httpHelper

def getSummonerMatchHistory(summonerId):
    print ('Fetching Summoner Match History.')
    if isinstance(summonerId, int):
        summonerId=str(summonerId)
    url = 'https://na.api.pvp.net/api/lol/na/v1.3/game/by-summoner/' + summonerId + '/recent'
    data = httpHelper.makeGetRequest(url)
    return data


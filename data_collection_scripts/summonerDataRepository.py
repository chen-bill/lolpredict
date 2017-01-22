import pprint
import atexit
import mysql.connector
import secrets
from datetime import datetime
import json
import pdb
import requests
import httpHelper

pp = pprint.PrettyPrinter(indent=2)

NUM_SQL_COLUMNS = 21

TABLE_NAME = 'summonerChampionStats'

SQL_KEYS = [
	'summonerId', 
	'championId', 
	'totalSessionsPlayed', 
	'totalSessionsLost', 
	'totalSessionsWon', 
	'totalChampionKills', 
	'totalDamageDealt', 
	'totalDamageTaken', 
	'mostChampionKillsPerSession',
	'totalMinionKills',
	'totalDoubleKills', 
	'totalTripleKills',
	'totalQuadraKills',
	'totalPentaKills',
	'totalUnrealKills',
	'totalDeathsPerSession',
	'totalGoldEarned',
	'mostSpellsCast',
	'totalTurretsKilled',
	'totalPhysicalDamageDealt',
	'totalMagicDamageDealt',
	'totalFirstBlood',
	'totalAssists',
	'maxChampionsKilled',
	'maxNumDeaths'
]

CNX = mysql.connector.connect(
        user='root', 
        password='password',
        host='localhost',
        database='loldata')

addSummonerChampStat = ('INSERT INTO ' + TABLE_NAME + ' (id, ' + ','.join(SQL_KEYS) + 
        ') VALUES (%(id)s, ' + ','.join(['%(' + i + ')s' for i in SQL_KEYS])  + ')')

updateSummonerChampStat = ('UPDATE ' + TABLE_NAME + ' set ' + 
        ','.join([ i + ' = %(' + i + ')s' for i in SQL_KEYS]) + 
        ' where id=%(id)s')

def getDeleteAllForSummonerQuery(summonerId):
    return 'DELETE FROM ' + TABLE_NAME + ' WHERE summonerId=' + str(summonerId)

def createSummonerChampStatDto(summonerStat, summonerId):
    summonerDtos = []
    for championStat in summonerStat['champions']:
        summonerChampStatDto = {}
        summonerChampStatDto['summonerId'] = summonerId
        summonerChampStatDto['championId'] = championStat['id']
        summonerChampStatDto['updatedOn'] = datetime.utcnow()
        for key,val in championStat['stats'].iteritems():
            summonerChampStatDto[key] = val
        summonerChampStatDto['id'] = str(summonerChampStatDto['summonerId']) + '-' + str(summonerChampStatDto['championId'])
        summonerDtos.append(summonerChampStatDto)
    return summonerDtos

def fetchNewChampDto(summonerId):
    url = 'https://na.api.pvp.net/api/lol/na/v1.3/stats/by-summoner/' + str(summonerId) + '/ranked'
    data = httpHelper.makeGetRequest(url)
    if data is None:
        return None
    else:
        return createSummonerChampStatDto(data, summonerId)

def updateSummonerData(summonerId):
    print ('Updating data for summoner ' + str(summonerId))
    summonerChampData = fetchNewChampDto(summonerId)
    #http helper will return None when there is 404
    if summonerChampData is None:
        return
    try:
        cursor = CNX.cursor()
        #purge old data
        #TODO check last updated time and purge only if not the same
        cursor.execute(getDeleteAllForSummonerQuery(summonerId))
        for singleChampData in summonerChampData:
            #TODO does 'total' need too be separated from the rest?
            # if singleChampData['championId'] == 0:
                # #champId 0 is total over all games
                # cursor.execute(addTotalSummonerChampStat, singleChampData)
            # else:
            cursor.execute(addSummonerChampStat, singleChampData)
            print ('Updating ' + singleChampData['id'])
        CNX.commit()
    except Exception as e:
        print 'ERROR - updateSummonerData: ' + str(e)
    finally:
        cursor.close()
        print ('Finished updating summonerChampionStats')

def closeDB():
    CNX.close()

atexit.register(closeDB)

if __name__ == '__main__':
    #used for testing purposes
    updateSummonerData(90515)

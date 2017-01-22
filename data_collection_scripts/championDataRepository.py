import mysql.connector
import atexit
from datetime import datetime
import json
import pdb
import re
import urllib2
from bs4 import BeautifulSoup as bs

CHAMPION_STATS_REGEX = 'matchupData.stats = (.*])'
CHAMPION_ID_REGEX = 'var champData = (.*);'
NUM_SQL_COLUMNS = 21
SQL_KEYS = ['champId', 'role', 'title', 'winPercent', 'playPercent', 'banRate', 'experience', 'kills', 'deaths', 'assists', 'totalDamageDealtToChampions', 
        'totalDamageTaken', 'totalHeal', 'largestKillingSpree', 'minionsKilled', 'neutralMinionsKilledTeamJungle', 'neutralMinionsKilledEnemyJungle', 'goldEarned', 'overallPosition', 
        'overallPositionChange', 'updatedOn']
CNX = mysql.connector.connect(
        user='root', 
        password='password',
        host='localhost',
        database='loldata')

addChampion = ('INSERT INTO globalChampionAverages (id, ' + ','.join(SQL_KEYS) + 
        ') VALUES (%(id)s, ' + ','.join(['%(' + i + ')s' for i in SQL_KEYS])  + ')')

updateChampion = ('UPDATE globalChampionAverages set ' + 
        ','.join([ i + ' = %(' + i + ')s' for i in SQL_KEYS]) + 
        ' where id=%(id)s')

def createChampionDto(championStat, championIdDict):
    champDto = {}
    champDto['role'] = championStat['role']
    champDto['title'] = championStat['title']
    champDto['key'] = championStat['key']
    champDto['champId'] = int(championIdDict[championStat['key']])
    champDto['updatedOn'] = datetime.utcnow()
    for key,val in championStat['general'].iteritems():
        champDto[key] = val
    champDto['id'] = str(champDto['champId']) + champDto['role']
    return champDto

def fetchRawChampionGGPage():
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    r = opener.open('http://champion.gg/statistics/').read()
    soup = bs(r, 'html.parser')
    return soup

def fetchChampionStats():
    stringData = str(fetchRawChampionGGPage())
    realData = re.search(CHAMPION_STATS_REGEX, stringData)
    return json.loads(realData.group(1))

def fetchDataChampionIds():
    stringData = str(fetchRawChampionGGPage())
    realData = re.search(CHAMPION_ID_REGEX, stringData)
    return json.loads(realData.group(1))

def updateChampionData():
    championIdDict = fetchDataChampionIds()
    championStats = fetchChampionStats()
    try:
        cursor = CNX.cursor()
        for championStat in championStats:
            dto = createChampionDto(championStat, championIdDict)
            searchQuery = 'SELECT * from globalChampionAverages where id="' + dto['id'] + '"'
            cursor.execute(searchQuery)
            existingEntry = cursor.fetchone()
            if existingEntry == None:
                print ('creating ' + dto['title'] + " id=" + dto['id'])
                cursor.execute(addChampion, dto)
                CNX.commit()
            else:
                print ('updating ' + dto['title'] + " id=" + dto['id'])
                cursor.execute(updateChampion, dto)
                # pdb.set_trace()
                CNX.commit()
    except Exception as e:
        print ("ERROR - ChampionDataRepository: " + str(e))
    finally:
        cursor.close()

def closeDb():
    CNX.close()

atexit.register(closeDb)

if __name == '__main__':
    updateChampionData()

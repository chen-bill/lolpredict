import pprint
import atexit
import mysql.connector
import secrets
from datetime import datetime
import json
import pdb
import httpHelper
import summonerRepository

pp = pprint.PrettyPrinter(indent=2)

TABLE_NAME = 'matchResults'

SQL_KEYS = [
    'region',
    'season',
    'matchVersion',
    'bTopId',
    'bTopChampId',
    'bJungleId',
    'bJungleChampId',
    'bMidId',
    'bMidChampId',
    'bBotId',
    'bBotChampId',
    'bSupportId',
    'bSupportChampId',
    'pTopId',
    'pTopChampId',
    'pJungleId',
    'pJungleChampId',
    'pMidId',
    'pMidChampId',
    'pBotId',
    'pBotChampId',
    'pSupportId',
    'pSupportChampId',
    'bWin',
    'matchCreation',
    'createdOn'
]

CNX = mysql.connector.connect(
        user='root', 
        password='password',
        host='localhost',
        database='loldata')

addMatchResultSQL = ('INSERT INTO ' + TABLE_NAME + ' (id, ' + ','.join(SQL_KEYS) + 
        ') VALUES (%(id)s, ' + ','.join(['%(' + i + ')s' for i in SQL_KEYS])  + ')')

def fetchMatchResultData(matchId):
    url = 'https://na.api.pvp.net/api/lol/na/v2.2/match/' + str(matchId) + '?api_key=' + secrets.getRiotAPIKey()
    data = httpHelper.makeGetRequest(url)
    return data

def createMatchDto(rawMatchResult):
    matchDto = {}
    matchDto['id'] = rawMatchResult['matchId']
    matchDto['region'] = rawMatchResult['region']
    matchDto['season'] = rawMatchResult['season']
    matchDto['matchVersion'] = rawMatchResult['matchVersion']
    #dont care about milliseconds
    matchDto['matchCreation'] = datetime.fromtimestamp(rawMatchResult['matchCreation']/1000)
    matchDto['createdOn'] = datetime.utcnow()
    #TODO error proof this. This assumes that participants and partipant identities are in the same order
    #it is for all tested results, but its good to check
    for participantIndex in range(10):
        participant = rawMatchResult['participants'][participantIndex]
        participantIdentity = rawMatchResult['participantIdentities'][participantIndex]
        addSummonerToDto(matchDto, participant, participantIdentity, rawMatchResult)
    addBlueWin(matchDto, rawMatchResult)
    return matchDto

def addBlueWin(matchDto, rawMatchResult):
    if rawMatchResult['teams'][0]['winner']:
        matchDto['bWin'] = True
    else:
        matchDto['bWin'] = False

def addSummonerToDto(matchDto, participant, participantIdentity, rawMatchResult):
    summonerId = participantIdentity['player']['summonerId']
    championId = participant['championId']
    if participant['timeline']['lane'] == 'TOP' and participant['teamId'] == 100:
        addBTop(matchDto, summonerId, championId)
    elif participant['timeline']['lane'] == 'JUNGLE' and participant['teamId'] == 100:
        addBJungle(matchDto, summonerId, championId)
    elif participant['timeline']['lane'] == 'MIDDLE' and participant['teamId'] == 100:
        addBMid(matchDto, summonerId, championId)
    #TODO fix this
    #Perhaps check damange dealt 
    elif participant['timeline']['lane'] == 'BOTTOM' and participant['timeline']['role'] == 'DUO_SUPPORT' and participant['teamId'] == 100:
        addBSupport(matchDto, summonerId, championId)
    elif participant['timeline']['lane'] == 'BOTTOM' and participant['timeline']['role'] == 'DUO_CARRY' and participant['teamId'] == 100:
        addBBottom(matchDto, summonerId, championId)
    #idk why riot does this, but they do so we have to accomodate for this
    elif participant['timeline']['lane'] == 'BOTTOM' and participant['timeline']['role'] == 'DUO' and participant['teamId'] == 100:
        addAmbiguousBottom(matchDto, participant, participantIdentity, rawMatchResult)

    elif participant['timeline']['lane'] == 'TOP' and participant['teamId'] == 200:
        addPTop(matchDto, summonerId, championId)
    elif participant['timeline']['lane'] == 'JUNGLE' and participant['teamId'] == 200:
        addPJungle(matchDto, summonerId, championId)
    elif participant['timeline']['lane'] == 'MIDDLE' and participant['teamId'] == 200:
        addPMid(matchDto, summonerId, championId)
    elif participant['timeline']['lane'] == 'BOTTOM' and participant['timeline']['role'] == 'DUO_SUPPORT' and participant['teamId'] == 200:
        addPSupport(matchDto, summonerId, championId)
    elif participant['timeline']['lane'] == 'BOTTOM' and participant['timeline']['role'] == 'DUO_CARRY' and participant['teamId'] == 200:
        addPBottom(matchDto, summonerId, championId)
    elif participant['timeline']['lane'] == 'BOTTOM' and participant['timeline']['role'] == 'DUO' and participant['teamId'] == 200:
        addAmbiguousBottom(matchDto, participant, participantIdentity, rawMatchResult)
    return

def findDuoPartner(participant, participantIdentity, rawMatchResult):
    if participantIdentity['participantId'] <= 5:
        for i in [i for i in range(5) if i != (participantIdentity['participantId'] - 1)]:
            if rawMatchResult['participants'][i]['timeline']['lane'] == 'BOTTOM':
                return rawMatchResult['participants'][i]
    else:
        for i in [i for i in range(5, 10) if i != (participantIdentity['participantId'] - 1)]:
            if rawMatchResult['participants'][i]['timeline']['lane'] == 'BOTTOM':
                return rawMatchResult['participants'][i]

def addAmbiguousBottom(matchDto, participant, participantIdentity, rawMatchResult):
    summonerId = participantIdentity['player']['summonerId']
    championId = participant['championId']
    duoPartner = findDuoPartner(participant, participantIdentity, rawMatchResult)
    currentSummoner = rawMatchResult['participants'][participantIdentity['participantId'] - 1]
    if currentSummoner['stats']['totalDamageDealt'] >= duoPartner['stats']['totalDamageDealt']:
        if participant['teamId'] == 100:
            addBBottom(matchDto, summonerId, championId)
        else:
            addPBottom(matchDto, summonerId, championId)
    else:
        if participant['teamId'] == 100:
            addBSupport(matchDto, summonerId, championId)
        else:
            addPSupport(matchDto, summonerId, championId)
    return
    
def addBTop(matchDto, summonerId, championId):
    matchDto['bTopId'] = summonerId
    matchDto['bTopChampId'] = championId
    return

def addBJungle(matchDto, summonerId, championId):
    matchDto['bJungleId'] = summonerId
    matchDto['bJungleChampId'] = championId
    return

def addBMid(matchDto, summonerId, championId):
    matchDto['bMidId'] = summonerId
    matchDto['bMidChampId'] = championId
    return

def addBBottom(matchDto, summonerId, championId):
    matchDto['bBotId'] = summonerId
    matchDto['bBotChampId'] = championId
    return

def addBSupport(matchDto, summonerId, championId):
    matchDto['bSupportId'] = summonerId
    matchDto['bSupportChampId'] = championId
    return

def addPTop(matchDto, summonerId, championId):
    matchDto['pTopId'] = summonerId
    matchDto['pTopChampId'] = championId
    return

def addPJungle(matchDto, summonerId, championId):
    matchDto['pJungleId'] = summonerId
    matchDto['pJungleChampId'] = championId
    return

def addPMid(matchDto, summonerId, championId):
    matchDto['pMidId'] = summonerId
    matchDto['pMidChampId'] = championId
    return

def addPBottom(matchDto, summonerId, championId):
    matchDto['pBotId'] = summonerId
    matchDto['pBotChampId'] = championId
    return

def addPSupport(matchDto, summonerId, championId):
    matchDto['pSupportId'] = summonerId
    matchDto['pSupportChampId'] = championId
    return

def saveMatchToDb(matchDto):
    try:
        cursor = CNX.cursor()
        cursor.execute(addMatchResultSQL, matchDto)
        CNX.commit()
        print ('Successfully updated match # ' + str(matchDto['id']))
    except Exception as e:
        CNX.rollback()
        print ('ERROR: ' + str(e) + ' for matchId: ' + str(matchDto['id']))
    finally:
        cursor.close()

def isPlatOrHigher(rawData):
    rankMap = findDominantRank(rawData)
    numValidRanks = 0
    for k, v in rankMap.items():
        if k=='PLATINUM' or k=='DIAMOND' or k=='MASTER' or k=='CHALLENGER':
            #save to summoners here
            numValidRanks += v
    return numValidRanks > 5

def findDominantRank(rawData):
    rankMap = {}
    # printAllKeys(rawData)
    if 'participants' not in rawData:
        print ('ERROR findDominantRank - No participants field')
        return 
    for participant in rawData['participants']:
        if participant['highestAchievedSeasonTier'] not in rankMap:
            rankMap[participant['highestAchievedSeasonTier']] = 1
        else:
            rankMap[participant['highestAchievedSeasonTier']] += 1
    return rankMap

def printAllKeys(iterMap):
    print iterMap
    print ('Printing Keys')
    for k,v in iterMap.iteritems():
        print (k)

def getMatchByIdSql(matchId):
    try:
        cursor = CNX.cursor()
        cursor.execute('SELECT * FROM ' + TABLE_NAME + ' where id=' + str(matchId))
        return cursor.fetchone()
    except Exception as e:
        print ('ERROR - getMatchByIdSql: ' + str(e))
    finally:
        cursor.close()

def checkIfMatchExists(matchId):
    return getMatchByIdSql(matchId) is not None

def closeDB():
    CNX.close()

atexit.register(closeDB)

#main method
def createMatchResult(matchId):
    print ("Creating Match Result for " + str(matchId))
    rawData = fetchMatchResultData(matchId)

    #adds all summoners in the match db
    summonerRepository.addSummonersToDb(rawData)
    #accpeting both flex and solo 5v5
    if isPlatOrHigher(rawData) and (rawData['queueType']=='RANKED_FLEX_SR' or rawData['queueType']=='TEAM_BUILDER_RANKED_SOLO'):
        matchDto = createMatchDto(rawData)
        saveMatchToDb(matchDto)
    else:
        print ("Skipping Match: Below Platinum")

if __name__ == '__main__':
    #used for testing purposes
    createMatchResult(2397221818)



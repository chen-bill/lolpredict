import mysql.connector
import atexit
import pdb
from datetime import datetime, timedelta

TABLE_NAME = 'Summoners'
SQL_KEYS = ['summonerName', 'highestAchievedSeasonTier', 'matchHistoryUri', 'updatedOn']

CNX = mysql.connector.connect(
        user='root', 
        password='password',
        host='localhost',
        database='loldata')

addSummonerSql = ('INSERT INTO ' + TABLE_NAME + ' (id, ' + ','.join(SQL_KEYS) + 
        ') VALUES (%(id)s, ' + ','.join(['%(' + i + ')s' for i in SQL_KEYS])  + ') \
        ON DUPLICATE KEY UPDATE id=%(id)s')

def getResetSummonerUpdatedOnSql(summonerId):
    return 'UPDATE Summoners SET updatedOn="' + str(datetime.utcnow()) + '" WHERE id="' + str(summonerId) + '"';

def resetSummonerUpdatedOn(summonerId):
    try:
        cursor = CNX.cursor()
        cursor.execute(getResetSummonerUpdatedOnSql(summonerId))
        CNX.commit()
    except Exception as e:
        print ('ERROR - resetUpdatedOn: ' + str(e))
    finally:
        cursor.close()

def getSummonerQuerySQL():
    #only checks the summoner's match history if it has been at least a day since last check
    checkedTime = datetime.utcnow() - timedelta(days=1)
    return 'SELECT * FROM Summoners WHERE \
            (highestAchievedSeasonTier="PLATINUM" or highestAchievedSeasonTier="DIAMOND" \
            or highestAchievedSeasonTier="MASTER" or highestAchievedSeasonTier="CHALLENGER")\
            AND (updatedOn<"' + str(checkedTime) + '" or updatedOn IS NULL) ORDER BY updatedOn'

def getAllMissingMatchResultSummonerIds():
    sql = 'SELECT allChampIds.id from (SELECT bTopId as id FROM matchResults \
        UNION SELECT bJungleId FROM matchResults \
        UNION SELECT bMidId FROM matchResults \
        UNION SELECT bBotId FROM matchResults \
        UNION SELECT bSupportId FROM matchResults \
        UNION SELECT pTopId FROM matchResults \
        UNION SELECT pJungleId FROM matchResults \
        UNION SELECT pMidId FROM matchResults \
        UNION SELECT pBotId FROM matchResults \
        UNION SELECT pSupportId FROM matchResults) allChampIds \
        LEFT JOIN summonerChampionStats on \
        allChampIds.id = summonerChampionStats.summonerId \
        WHERE summonerChampionStats.id is null'
    try:
        cursor = CNX.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print ('ERROR getAllMissingMatchResultSummonerIds: ' + str(e))
    finally:
        cursor.close()

#takes the match result as input and adds summoners if required
def addSummonersToDb(rawMatchResult):
    if 'participantIdentities' in rawMatchResult:
        participantIdentities = rawMatchResult['participantIdentities']
        for summoner in participantIdentities:
            summonerDto = getSummonerDto(summoner, rawMatchResult)
            cursor = CNX.cursor()
            try:
                #add summoner sql will prevent duplicates
                cursor.execute(addSummonerSql, summonerDto)
                CNX.commit()
                print ('Successfully added summoner id: ' + str(summoner['player']['summonerId']) + ' name: ' + summoner['player']['summonerName'])
            except Exception as e:
                CNX.rollback()
                # this will throw encoding error for certain characters
                # print ('ERROR: ' + str(e) + ' for summoner id: ' + str(summoner['player']['summonerId']) + ' name: ' + summoner['player']['summonerName'])
                print ('ERROR: ' + str(e) + ' for summoner id: ' + str(summoner['player']['summonerId']))
            finally:
                cursor.close()
    else:
        print('Error adding summoners to db for data: ' + str(rawMatchResult))
        exit()

def getSummonerDto(participantIdentity, rawMatchResult):
    summonerDto = {
        'id': participantIdentity['player']['summonerId'],
        'summonerName': participantIdentity['player']['summonerName'],
        'highestAchievedSeasonTier': getHighestAchievedSeasonTier(participantIdentity, rawMatchResult),
        'matchHistoryUri': participantIdentity['player']['matchHistoryUri'],
        # 'updatedOn': datetime.utcnow()
        'updatedOn': None
    }
    return summonerDto

def getHighestAchievedSeasonTier(participantIdentity, rawMatchResult):
    #index is one less than the participant identity
    participantIndex = participantIdentity['participantId'] - 1
    return rawMatchResult['participants'][participantIndex]['highestAchievedSeasonTier']

def closeDB():
    CNX.close()

atexit.register(closeDB)

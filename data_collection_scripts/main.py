import pprint
import atexit
import redis
import mysql.connector
import secrets
from datetime import datetime, timedelta
import json
import pdb
import httpHelper
import summonerRepository
import matchHistoryRepository
import matchResultsRepository
import summonerChampionStatsRepository

pp = pprint.PrettyPrinter(indent=2)

TABLE_NAME = 'matchResults'

#look for plat+ players in summoner db
CNX = mysql.connector.connect(
        user='root', 
        password='password',
        host='localhost',
        database='loldata')

def getAllData():
    # try:
        #if no buffered, will throw error on close
        cursor = CNX.cursor(buffered=True)
        # matchCheckCursor = CNX.cursor(buffered=True)
        cursor.execute(summonerRepository.getSummonerQuerySQL())
        checkedSummoner = cursor.fetchone()
        while (checkedSummoner is not None):
            summonerMatchHistory = matchHistoryRepository.getSummonerMatchHistory(checkedSummoner[0])
            print ('Checking ' + str(summonerMatchHistory['summonerId']) + '\'s match history.')
            for game in summonerMatchHistory['games']:
                if not (game['subType'] == 'RANKED_FLEX_SR' or game['subType'] == 'RANKED_SOLO_5x5'):
                    print (str(game['gameId']) + ' is not a ranked game, skipping.')
                elif matchResultsRepository.checkIfMatchExists(game['gameId']):
                    print ('Game already exists in database, skipping.')
                else: 
                    print ('Getting match ' + str(game['gameId']))
                    matchResultsRepository.createMatchResult(game['gameId'])
                    #finds all the new champions and add their stats in the db
                    summonerChampionStatsRepository.getSummonerChampionStats()
            #passes summoner id to resetSummonerUpdatedOn
            summonerRepository.resetSummonerUpdatedOn(checkedSummoner[0])
            checkedSummoner = cursor.fetchone()
            print ('Next summoner')
        print ('end of while loop')
    # except Exception as e:
        # print ('Main: ' + str(e))
    # finally:
        # cursor.close()

def closeDB():
    CNX.close()
atexit.register(closeDB)
        
print ('Starting Main Program.')
getAllData()



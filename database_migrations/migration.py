import mysql.connector
db = mysql.connector.connect(
        user='root', 
        password='password',
        host='localhost',
        database='loldata')
db.autocommit = False

def purge():
    cursor = db.cursor()
    try:
        cursor.execute("drop table globalChampionAverages")
    except Exception as e:
        db.rollback()
        print(e)
    finally:
        print('created globalChampionAverage table')

def closeDb():
    db.close()

#TODO upper camel case database names
def defineApiQueue():
    cursor = db.cursor()
    try:
        cursor.execute("create table apiQueue(id varchar(64), typeName varchar(64), \
                typeId long, primary key(id), CONSTRAINT fk_uniqueQueueItem UNIQUE (typeName, typeId(767)))")
        db.commit()
        print ('Successfully set up globalChampionAverages')
    except Exception as e:
        db.rollback()
        print('Error - apiQueue: ' + str(e))

def defineGlobalChampionAverages():
    cursor = db.cursor()
    try:
        cursor.execute("create table globalChampionAverages(id varchar(64), champId long, role varchar(64), title varchar(64), \
        winPercent float, playPercent float, banRate float, experience float, kills float, deaths float, assists float, \
        totalDamageDealtToChampions long, totalDamageTaken long, totalHeal long, largestKillingSpree long, minionsKilled int,\
        neutralMinionsKilledTeamJungle long, neutralMinionsKilledEnemyJungle long, goldEarned long, overallPosition long, overallPositionChange long, \
        updatedOn timestamp, primary key(id), CONSTRAINT fk_uniqueChamp UNIQUE (champId(767), role))")
        db.commit()
        print ('Successfully set up globalChampionAverages')
    except Exception as e:
        db.rollback()
        print('Error - globalChampionAverages: ' + str(e))

def defineSummoners():
    cursor = db.cursor()
    try:
        cursor.execute("create table Summoners(id long,summonerName varchar(64), \
                highestAchievedSeasonTier varchar(64), matchHistoryUri varchar(64), updatedOn datetime, primary key(id(767)))")
        db.commit()
        print ('Successfully set up Summoners')
    except Exception as e:
        db.rollback()
        print('Error - Summoners: ' + str(e))

def defineMatchResults():
    cursor = db.cursor()
    try:
        cursor.execute("create table matchResults(id long, \
        region varchar(64), \
        season varchar(64), \
        matchVersion varchar(64),\
        bTopId long,\
        bTopChampId long,\
        bJungleId long,\
        bJungleChampId long,\
        bMidId long,\
        bMidChampId long,\
        bBotId long,\
        bBotChampId long,\
        bSupportId long,\
        bSupportChampId long,\
        pTopId long,\
        pTopChampId long,\
        pJungleId long,\
        pJungleChampId long,\
        pMidId long,\
        pMidChampId long,\
        pBotId long,\
        pBotChampId long,\
        pSupportId long,\
        pSupportChampId long,\
        bWin bool,\
        matchCreation datetime,\
        createdOn datetime,\
        primary key(id(767)))")
        db.commit()
        print ('Successfully set up matchResult table')
    except Exception as e:
        db.rollback()
        print('Error - matchResults: ' + str(e))

def defineSummonerChampionStats():
    cursor = db.cursor()
    try:
        query = 'create table summonerChampionStats(' +\
            'id varchar(64), ' +\
            'summonerId long, ' +\
            'championId long, ' +\
            'totalSessionsPlayed long, ' +\
            'totalSessionsLost long, ' +\
            'totalSessionsWon long, ' +\
            'totalChampionKills long, ' +\
            'totalDamageDealt long, ' +\
            'totalDamageTaken long, ' +\
            'mostChampionKillsPerSession long,' +\
            'totalMinionKills long,' +\
            'totalDoubleKills long, ' +\
            'totalTripleKills long,' +\
            'totalQuadraKills long,' +\
            'totalPentaKills long,' +\
            'totalUnrealKills long,' +\
            'totalDeathsPerSession long,' +\
            'totalGoldEarned long,' +\
            'mostSpellsCast long,' +\
            'totalTurretsKilled long,' +\
            'totalPhysicalDamageDealt long,' +\
            'totalMagicDamageDealt long,' +\
            'totalFirstBlood long,' +\
            'totalAssists long,' +\
            'maxChampionsKilled long,' +\
            'maxNumDeaths long,' +\
            'updatedOn timestamp, primary key(id),' +\
            'CONSTRAINT fk_uniqueSummonerChampStat UNIQUE (summonerId(100), championId(100)))'
            #had to reduce fk constraint size because errors
        cursor.execute(query)
        db.commit()
        print ('Successfully set up summonerChampionStats table')
    except Exception as e:
        db.rollback()
        print('Error - SummonerChampionStats: ' + str(e))

def defineMatchData():
    cursor = db.cursor()
    try:
        query = 'create table summonerChampionStats(' +\
            'id varchar(64), ' +\
            'summonerId long, ' +\
            'championId long, ' +\
            'totalSessionsPlayed long, ' +\
            'totalSessionsLost long, ' +\
            'totalSessionsWon long, ' +\
            'totalChampionKills long, ' +\
            'totalDamageDealt long, ' +\
            'totalDamageTaken long, ' +\
            'mostChampionKillsPerSession long,' +\
            'totalMinionKills long,' +\
            'totalDoubleKills long, ' +\
            'totalTripleKills long,' +\
            'totalQuadraKills long,' +\
            'totalPentaKills long,' +\
            'totalUnrealKills long,' +\
            'totalDeathsPerSession long,' +\
            'totalGoldEarned long,' +\
            'mostSpellsCast long,' +\
            'totalTurretsKilled long,' +\
            'totalPhysicalDamageDealt long,' +\
            'totalMagicDamageDealt long,' +\
            'totalFirstBlood long,' +\
            'totalAssists long,' +\
            'maxChampionsKilled long,' +\
            'maxNumDeaths long,' +\
            'updatedOn timestamp, primary key(id),' +\
            'CONSTRAINT fk_uniqueSummonerChampStat UNIQUE (summonerId(767), championId(767)))'
        cursor.execute(query)
        db.commit()
        print ('Successfully set up summonerChampionStats table')
    except Exception as e:
        db.rollback()
        print('Error - matchData: ' + str(e))


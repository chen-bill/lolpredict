import numpy as np
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
from sklearn.cross_validation import train_test_split

DATAFRAME_SQL_QUERY = " \
    SELECT  \
        gca1.winPercent as bTopAverageWinPercent,  \
        gca1.playPercent as bTopAveragePlayPercent,  \
        gca1.banRate as bTopAverageBanRate,  \
        gca1.experience as bTopAverageExperience,  \
        gca1.kills as bTopAverageKills,  \
        gca1.deaths as bTopAverageDeaths,  \
        gca1.assists as bTopAverageAssists,  \
        gca1.totalDamageDealtToChampions as bTopAverageTotalDamageDealtToChampions,  \
        gca1.totalDamageTaken as bTopAverageTotalDamageTaken,   \
        gca1.totalHeal as bTopAverageTotalHeal, \
        gca1.largestKillingSpree as bTopAverageLargestKillingSpree,  \
        gca1.minionsKilled as bTopAverageMinionsKilled,  \
        gca1.neutralMinionsKilledTeamJungle as bTopAverageNeutralMinionsKilledTeamJungle,  \
        gca1.neutralMinionsKilledEnemyJungle as bTopAverageNeutralMinionsKilledEnemyJungle,  \
        gca1.goldEarned as bTopAverageGoldEarned,  \
        gca1.overallPosition as bTopAverageOverallPosition, \
    \
        gca2.winPercent as bJungleAverageWinPercent,  \
        gca2.playPercent as bJungleAveragePlayPercent,  \
        gca2.banRate as bJungleAverageBanRate,  \
        gca2.experience as bJungleAverageExperience,  \
        gca2.kills as bJungleAverageKills,  \
        gca2.deaths as bJungleAverageDeaths,  \
        gca2.assists as bJungleAverageAssists,  \
        gca2.totalDamageDealtToChampions as bJungleAverageTotalDamageDealtToChampions,  \
        gca2.totalDamageTaken as bJungleAverageTotalDamageTaken,   \
        gca2.totalHeal as bJungleAverageTotalHeal, \
        gca2.largestKillingSpree as bJungleAverageLargestKillingSpree,  \
        gca2.minionsKilled as bJungleAverageMinionsKilled,  \
        gca2.neutralMinionsKilledTeamJungle as bJungleAverageNeutralMinionsKilledTeamJungle,  \
        gca2.neutralMinionsKilledEnemyJungle as bJungleAverageNeutralMinionsKilledEnemyJungle,  \
        gca2.goldEarned as bJungleAverageGoldEarned,  \
        gca2.overallPosition as bJungleAverageOverallPosition, \
     \
        gca3.winPercent as bMidAverageWinPercent,  \
        gca3.playPercent as bMidAveragePlayPercent,  \
        gca3.banRate as bMidAverageBanRate,  \
        gca3.experience as bMidAverageExperience,  \
        gca3.kills as bMidAverageKills,  \
        gca3.deaths as bMidAverageDeaths,  \
        gca3.assists as bMidAverageAssists,  \
        gca3.totalDamageDealtToChampions as bMidAverageTotalDamageDealtToChampions,  \
        gca3.totalDamageTaken as bMidAverageTotalDamageTaken,   \
        gca3.totalHeal as bMidAverageTotalHeal, \
        gca3.largestKillingSpree as bMidAverageLargestKillingSpree,  \
        gca3.minionsKilled as bMidAverageMinionsKilled,  \
        gca3.neutralMinionsKilledTeamJungle as bMidAverageNeutralMinionsKilledTeamJungle,  \
        gca3.neutralMinionsKilledEnemyJungle as bMidAverageNeutralMinionsKilledEnemyJungle,  \
        gca3.goldEarned as bMidAverageGoldEarned,  \
        gca3.overallPosition as bMidAverageOverallPosition, \
     \
        gca4.winPercent as bBotAverageWinPercent,  \
        gca4.playPercent as bBotAveragePlayPercent,  \
        gca4.banRate as bBotAverageBanRate,  \
        gca4.experience as bBotAverageExperience,  \
        gca4.kills as bBotAverageKills,  \
        gca4.deaths as bBotAverageDeaths,  \
        gca4.assists as bBotAverageAssists,  \
        gca4.totalDamageDealtToChampions as bBotAverageTotalDamageDealtToChampions,  \
        gca4.totalDamageTaken as bBotAverageTotalDamageTaken,   \
        gca4.totalHeal as bBotAverageTotalHeal, \
        gca4.largestKillingSpree as bBotAverageLargestKillingSpree,  \
        gca4.minionsKilled as bBotAverageMinionsKilled,  \
        gca4.neutralMinionsKilledTeamJungle as bBotAverageNeutralMinionsKilledTeamJungle,  \
        gca4.neutralMinionsKilledEnemyJungle as bBotAverageNeutralMinionsKilledEnemyJungle,  \
        gca4.goldEarned as bBotAverageGoldEarned,  \
        gca4.overallPosition as bBotAverageOverallPosition, \
     \
        gca5.winPercent as bSupportAverageWinPercent,  \
        gca5.playPercent as bSupportAveragePlayPercent,  \
        gca5.banRate as bSupportAverageBanRate,  \
        gca5.experience as bSupportAverageExperience,  \
        gca5.kills as bSupportAverageKills,  \
        gca5.deaths as bSupportAverageDeaths,  \
        gca5.assists as bSupportAverageAssists,  \
        gca5.totalDamageDealtToChampions as bSupportAverageTotalDamageDealtToChampions,  \
        gca5.totalDamageTaken as bSupportAverageTotalDamageTaken,   \
        gca5.totalHeal as bSupportAverageTotalHeal, \
        gca5.largestKillingSpree as bSupportAverageLargestKillingSpree,  \
        gca5.minionsKilled as bSupportAverageMinionsKilled,  \
        gca5.neutralMinionsKilledTeamJungle as bSupportAverageNeutralMinionsKilledTeamJungle,  \
        gca5.neutralMinionsKilledEnemyJungle as bSupportAverageNeutralMinionsKilledEnemyJungle,  \
        gca5.goldEarned as bSupportAverageGoldEarned,  \
        gca5.overallPosition as bSupportAverageOverallPosition, \
     \
        gca6.winPercent as pTopAverageWinPercent,  \
        gca6.playPercent as pTopAveragePlayPercent,  \
        gca6.banRate as pTopAverageBanRate,  \
        gca6.experience as pTopAverageExperience,  \
        gca6.kills as pTopAverageKills,  \
        gca6.deaths as pTopAverageDeaths,  \
        gca6.assists as pTopAverageAssists,  \
        gca6.totalDamageDealtToChampions as pTopAverageTotalDamageDealtToChampions,  \
        gca6.totalDamageTaken as pTopAverageTotalDamageTaken,   \
        gca6.totalHeal as pTopAverageTotalHeal, \
        gca6.largestKillingSpree as pTopAverageLargestKillingSpree,  \
        gca6.minionsKilled as pTopAverageMinionsKilled,  \
        gca6.neutralMinionsKilledTeamJungle as pTopAverageNeutralMinionsKilledTeamJungle,  \
        gca6.neutralMinionsKilledEnemyJungle as pTopAverageNeutralMinionsKilledEnemyJungle,  \
        gca6.goldEarned as pTopAverageGoldEarned,  \
        gca6.overallPosition as pTopAverageOverallPosition, \
    \
        gca7.winPercent as pJungleAverageWinPercent,  \
        gca7.playPercent as pJungleAveragePlayPercent,  \
        gca7.banRate as pJungleAverageBanRate,  \
        gca7.experience as pJungleAverageExperience,  \
        gca7.kills as pJungleAverageKills,  \
        gca7.deaths as pJungleAverageDeaths,  \
        gca7.assists as pJungleAverageAssists,  \
        gca7.totalDamageDealtToChampions as pJungleAverageTotalDamageDealtToChampions,  \
        gca7.totalDamageTaken as pJungleAverageTotalDamageTaken,   \
        gca7.totalHeal as pJungleAverageTotalHeal, \
        gca7.largestKillingSpree as pJungleAverageLargestKillingSpree,  \
        gca7.minionsKilled as pJungleAverageMinionsKilled,  \
        gca7.neutralMinionsKilledTeamJungle as pJungleAverageNeutralMinionsKilledTeamJungle,  \
        gca7.neutralMinionsKilledEnemyJungle as pJungleAverageNeutralMinionsKilledEnemyJungle,  \
        gca7.goldEarned as pJungleAverageGoldEarned,  \
        gca7.overallPosition as pJungleAverageOverallPosition, \
         \
        gca8.winPercent as pMidAverageWinPercent,  \
        gca8.playPercent as pMidAveragePlayPercent,  \
        gca8.banRate as pMidAverageBanRate,  \
        gca8.experience as pMidAverageExperience,  \
        gca8.kills as pMidAverageKills,  \
        gca8.deaths as pMidAverageDeaths,  \
        gca8.assists as pMidAverageAssists,  \
        gca8.totalDamageDealtToChampions as pMidAverageTotalDamageDealtToChampions,  \
        gca8.totalDamageTaken as pMidAverageTotalDamageTaken,   \
        gca8.totalHeal as pMidAverageTotalHeal, \
        gca8.largestKillingSpree as pMidAverageLargestKillingSpree,  \
        gca8.minionsKilled as pMidAverageMinionsKilled,  \
        gca8.neutralMinionsKilledTeamJungle as pMidAverageNeutralMinionsKilledTeamJungle,  \
        gca8.neutralMinionsKilledEnemyJungle as pMidAverageNeutralMinionsKilledEnemyJungle,  \
        gca8.goldEarned as pMidAverageGoldEarned,  \
        gca8.overallPosition as pMidAverageOverallPosition, \
     \
        gca9.winPercent as pBotAverageWinPercent,  \
        gca9.playPercent as pBotAveragePlayPercent,  \
        gca9.banRate as pBotAverageBanRate,  \
        gca9.experience as pBotAverageExperience,  \
        gca9.kills as pBotAverageKills,  \
        gca9.deaths as pBotAverageDeaths,  \
        gca9.assists as pBotAverageAssists,  \
        gca9.totalDamageDealtToChampions as pBotAverageTotalDamageDealtToChampions,  \
        gca9.totalDamageTaken as pBotAverageTotalDamageTaken,   \
        gca9.totalHeal as pBotAverageTotalHeal, \
        gca9.largestKillingSpree as pBotAverageLargestKillingSpree,  \
        gca9.minionsKilled as pBotAverageMinionsKilled,  \
        gca9.neutralMinionsKilledTeamJungle as pBotAverageNeutralMinionsKilledTeamJungle,  \
        gca9.neutralMinionsKilledEnemyJungle as pBotAverageNeutralMinionsKilledEnemyJungle,  \
        gca9.goldEarned as pBotAverageGoldEarned,  \
        gca9.overallPosition as pBotAverageOverallPosition, \
    \
        gca10.winPercent as pSupportAverageWinPercent,  \
        gca10.playPercent as pSupportAveragePlayPercent,  \
        gca10.banRate as pSupportAverageBanRate,  \
        gca10.experience as pSupportAverageExperience,  \
        gca10.kills as pSupportAverageKills,  \
        gca10.deaths as pSupportAverageDeaths,  \
        gca10.assists as pSupportAverageAssists,  \
        gca10.totalDamageDealtToChampions as pSupportAverageTotalDamageDealtToChampions,  \
        gca10.totalDamageTaken as pSupportAverageTotalDamageTaken,   \
        gca10.totalHeal as pSupportAverageTotalHeal, \
        gca10.largestKillingSpree as pSupportAverageLargestKillingSpree,  \
        gca10.minionsKilled as pSupportAverageMinionsKilled,  \
        gca10.neutralMinionsKilledTeamJungle as pSupportAverageNeutralMinionsKilledTeamJungle,  \
        gca10.neutralMinionsKilledEnemyJungle as pSupportAverageNeutralMinionsKilledEnemyJungle,  \
        gca10.goldEarned as pSupportAverageGoldEarned,  \
        gca10.overallPosition as pSupportAverageOverallPosition, \
     \
        scs1.totalSessionsPlayed as bTopTotalSessionsPlayedOnChampion, \
        scs1.totalSessionsLost as bTopTotalSessionsLostOnChampion, \
        scs1.totalSessionsWon as bTopTotalSessionsWonOnChampion, \
        scs1.totalSessionsWon/scs1.totalSessionsPlayed as bTopWinRateOnChampion, \
        scs1.totalChampionKills/scs1.totalSessionsPlayed as bTopChampionKillsOnChampion, \
        scs1.totalDamageDealt/scs1.totalSessionsPlayed as bTopAverageDamageDealtOnChampion, \
        scs1.totalDamageTaken/scs1.totalSessionsPlayed as bTopAverageDamageTakenOnChampion, \
        scs1.totalMinionKills/scs1.totalSessionsPlayed as bTopAverageMinionKillsOnChampion, \
        scs1.totalDoubleKills/scs1.totalSessionsPlayed as bTopAverageDoubleKillsOnChampion, \
        scs1.totalTripleKills/scs1.totalSessionsPlayed as bTopAverageTripleKillsOnChampion, \
        scs1.totalQuadraKills/scs1.totalSessionsPlayed as bTopAverageQuadraKillsOnChampion, \
        scs1.totalPentaKills/scs1.totalSessionsPlayed as bTopAveragePentaKillsOnChampion, \
        scs1.totalUnrealKills/scs1.totalSessionsPlayed as bTopAverageUnrealKillsOnChampion, \
        scs1.totalDeathsPerSession/scs1.totalSessionsPlayed as bTopAverageDeathsPerSessionOnChampion, \
        scs1.totalGoldEarned/scs1.totalSessionsPlayed as bTopAverageGoldEarnedOnChampion, \
        scs1.totalTurretsKilled/scs1.totalSessionsPlayed as bTopAverageTurretsKilledOnChampion, \
        scs1.totalPhysicalDamageDealt/scs1.totalSessionsPlayed as bTopAveragePhysicalDamangeDealtOnChampion, \
        scs1.totalMagicDamageDealt/scs1.totalSessionsPlayed as bTopAverageMagicDamageDealthOnChampion, \
        scs1.totalFirstBlood/scs1.totalSessionsPlayed as bTopAverageFirstBloodOnChampion, \
        scs1.totalAssists/scs1.totalSessionsPlayed as bTopAverageAssits, \
        \
        scs2.totalSessionsPlayed as bJungleTotalSessionsPlayedOnChampion, \
        scs2.totalSessionsLost as bJungleTotalSessionsLostOnChampion, \
        scs2.totalSessionsWon as bJungleTotalSessionsWonOnChampion, \
        scs2.totalSessionsWon/scs2.totalSessionsPlayed as bJungleWinRateOnChampion, \
        scs2.totalChampionKills/scs2.totalSessionsPlayed as bJungleChampionKillsOnChampion, \
        scs2.totalDamageDealt/scs2.totalSessionsPlayed as bJungleAverageDamageDealtOnChampion, \
        scs2.totalDamageTaken/scs2.totalSessionsPlayed as bJungleAverageDamageTakenOnChampion, \
        scs2.totalMinionKills/scs2.totalSessionsPlayed as bJungleAverageMinionKillsOnChampion, \
        scs2.totalDoubleKills/scs2.totalSessionsPlayed as bJungleAverageDoubleKillsOnChampion, \
        scs2.totalTripleKills/scs2.totalSessionsPlayed as bJungleAverageTripleKillsOnChampion, \
        scs2.totalQuadraKills/scs2.totalSessionsPlayed as bJungleAverageQuadraKillsOnChampion, \
        scs2.totalPentaKills/scs2.totalSessionsPlayed as bJungleAveragePentaKillsOnChampion, \
        scs2.totalUnrealKills/scs2.totalSessionsPlayed as bJungleAverageUnrealKillsOnChampion, \
        scs2.totalDeathsPerSession/scs2.totalSessionsPlayed as bJungleAverageDeathsPerSessionOnChampion, \
        scs2.totalGoldEarned/scs2.totalSessionsPlayed as bJungleAverageGoldEarnedOnChampion, \
        scs2.totalTurretsKilled/scs2.totalSessionsPlayed as bJungleAverageTurretsKilledOnChampion, \
        scs2.totalPhysicalDamageDealt/scs2.totalSessionsPlayed as bJungleAveragePhysicalDamangeDealtOnChampion, \
        scs2.totalMagicDamageDealt/scs2.totalSessionsPlayed as bJungleAverageMagicDamageDealthOnChampion, \
        scs2.totalFirstBlood/scs2.totalSessionsPlayed as bJungleAverageFirstBloodOnChampion, \
        scs2.totalAssists/scs2.totalSessionsPlayed as bJungleAverageAssits, \
         \
        scs3.totalSessionsPlayed as bMidTotalSessionsPlayedOnChampion, \
        scs3.totalSessionsLost as bMidTotalSessionsLostOnChampion, \
        scs3.totalSessionsWon as bMidTotalSessionsWonOnChampion, \
        scs3.totalSessionsWon/scs3.totalSessionsPlayed as bMidWinRateOnChampion, \
        scs3.totalChampionKills/scs3.totalSessionsPlayed as bMidChampionKillsOnChampion, \
        scs3.totalDamageDealt/scs3.totalSessionsPlayed as bMidAverageDamageDealtOnChampion, \
        scs3.totalDamageTaken/scs3.totalSessionsPlayed as bMidAverageDamageTakenOnChampion, \
        scs3.totalMinionKills/scs3.totalSessionsPlayed as bMidAverageMinionKillsOnChampion, \
        scs3.totalDoubleKills/scs3.totalSessionsPlayed as bMidAverageDoubleKillsOnChampion, \
        scs3.totalTripleKills/scs3.totalSessionsPlayed as bMidAverageTripleKillsOnChampion, \
        scs3.totalQuadraKills/scs3.totalSessionsPlayed as bMidAverageQuadraKillsOnChampion, \
        scs3.totalPentaKills/scs3.totalSessionsPlayed as bMidAveragePentaKillsOnChampion, \
        scs3.totalUnrealKills/scs3.totalSessionsPlayed as bMidAverageUnrealKillsOnChampion, \
        scs3.totalDeathsPerSession/scs3.totalSessionsPlayed as bMidAverageDeathsPerSessionOnChampion, \
        scs3.totalGoldEarned/scs3.totalSessionsPlayed as bMidAverageGoldEarnedOnChampion, \
        scs3.totalTurretsKilled/scs3.totalSessionsPlayed as bMidAverageTurretsKilledOnChampion, \
        scs3.totalPhysicalDamageDealt/scs3.totalSessionsPlayed as bMidAveragePhysicalDamangeDealtOnChampion, \
        scs3.totalMagicDamageDealt/scs3.totalSessionsPlayed as bMidAverageMagicDamageDealthOnChampion, \
        scs3.totalFirstBlood/scs3.totalSessionsPlayed as bMidAverageFirstBloodOnChampion, \
        scs3.totalAssists/scs3.totalSessionsPlayed as bMidAverageAssits, \
         \
        scs4.totalSessionsPlayed as bBottomTotalSessionsPlayedOnChampion, \
        scs4.totalSessionsLost as bBottomTotalSessionsLostOnChampion, \
        scs4.totalSessionsWon as bBottomTotalSessionsWonOnChampion, \
        scs4.totalSessionsWon/scs4.totalSessionsPlayed as bBottomWinRateOnChampion, \
        scs4.totalChampionKills/scs4.totalSessionsPlayed as bBottomChampionKillsOnChampion, \
        scs4.totalDamageDealt/scs4.totalSessionsPlayed as bBottomAverageDamageDealtOnChampion, \
        scs4.totalDamageTaken/scs4.totalSessionsPlayed as bBottomAverageDamageTakenOnChampion, \
        scs4.totalMinionKills/scs4.totalSessionsPlayed as bBottomAverageMinionKillsOnChampion, \
        scs4.totalDoubleKills/scs4.totalSessionsPlayed as bBottomAverageDoubleKillsOnChampion, \
        scs4.totalTripleKills/scs4.totalSessionsPlayed as bBottomAverageTripleKillsOnChampion, \
        scs4.totalQuadraKills/scs4.totalSessionsPlayed as bBottomAverageQuadraKillsOnChampion, \
        scs4.totalPentaKills/scs4.totalSessionsPlayed as bBottomAveragePentaKillsOnChampion, \
        scs4.totalUnrealKills/scs4.totalSessionsPlayed as bBottomAverageUnrealKillsOnChampion, \
        scs4.totalDeathsPerSession/scs4.totalSessionsPlayed as bBottomAverageDeathsPerSessionOnChampion, \
        scs4.totalGoldEarned/scs4.totalSessionsPlayed as bBottomAverageGoldEarnedOnChampion, \
        scs4.totalTurretsKilled/scs4.totalSessionsPlayed as bBottomAverageTurretsKilledOnChampion, \
        scs4.totalPhysicalDamageDealt/scs4.totalSessionsPlayed as bBottomAveragePhysicalDamangeDealtOnChampion, \
        scs4.totalMagicDamageDealt/scs4.totalSessionsPlayed as bBottomAverageMagicDamageDealthOnChampion, \
        scs4.totalFirstBlood/scs4.totalSessionsPlayed as bBottomAverageFirstBloodOnChampion, \
        scs4.totalAssists/scs4.totalSessionsPlayed as bBottomAverageAssits, \
         \
        scs5.totalSessionsPlayed as bSupportTotalSessionsPlayedOnChampion, \
        scs5.totalSessionsLost as bSupportTotalSessionsLostOnChampion, \
        scs5.totalSessionsWon as bSupportTotalSessionsWonOnChampion, \
        scs5.totalSessionsWon/scs5.totalSessionsPlayed as bSupportWinRateOnChampion, \
        scs5.totalChampionKills/scs5.totalSessionsPlayed as bSupportChampionKillsOnChampion, \
        scs5.totalDamageDealt/scs5.totalSessionsPlayed as bSupportAverageDamageDealtOnChampion, \
        scs5.totalDamageTaken/scs5.totalSessionsPlayed as bSupportAverageDamageTakenOnChampion, \
        scs5.totalMinionKills/scs5.totalSessionsPlayed as bSupportAverageMinionKillsOnChampion, \
        scs5.totalDoubleKills/scs5.totalSessionsPlayed as bSupportAverageDoubleKillsOnChampion, \
        scs5.totalTripleKills/scs5.totalSessionsPlayed as bSupportAverageTripleKillsOnChampion, \
        scs5.totalQuadraKills/scs5.totalSessionsPlayed as bSupportAverageQuadraKillsOnChampion, \
        scs5.totalPentaKills/scs5.totalSessionsPlayed as bSupportAveragePentaKillsOnChampion, \
        scs5.totalUnrealKills/scs5.totalSessionsPlayed as bSupportAverageUnrealKillsOnChampion, \
        scs5.totalDeathsPerSession/scs5.totalSessionsPlayed as bSupportAverageDeathsPerSessionOnChampion, \
        scs5.totalGoldEarned/scs5.totalSessionsPlayed as bSupportAverageGoldEarnedOnChampion, \
        scs5.totalTurretsKilled/scs5.totalSessionsPlayed as bSupportAverageTurretsKilledOnChampion, \
        scs5.totalPhysicalDamageDealt/scs5.totalSessionsPlayed as bSupportAveragePhysicalDamangeDealtOnChampion, \
        scs5.totalMagicDamageDealt/scs5.totalSessionsPlayed as bSupportAverageMagicDamageDealthOnChampion, \
        scs5.totalFirstBlood/scs5.totalSessionsPlayed as bSupportAverageFirstBloodOnChampion, \
        scs5.totalAssists/scs5.totalSessionsPlayed as bSupportAverageAssits, \
         \
        scs6.totalSessionsPlayed as pTopTotalSessionsPlayedOnChampion, \
        scs6.totalSessionsLost as pTopTotalSessionsLostOnChampion, \
        scs6.totalSessionsWon as pTopTotalSessionsWonOnChampion, \
        scs6.totalSessionsWon/scs6.totalSessionsPlayed as pTopWinRateOnChampion, \
        scs6.totalChampionKills/scs6.totalSessionsPlayed as pTopChampionKillsOnChampion, \
        scs6.totalDamageDealt/scs6.totalSessionsPlayed as pTopAverageDamageDealtOnChampion, \
        scs6.totalDamageTaken/scs6.totalSessionsPlayed as pTopAverageDamageTakenOnChampion, \
        scs6.totalMinionKills/scs6.totalSessionsPlayed as pTopAverageMinionKillsOnChampion, \
        scs6.totalDoubleKills/scs6.totalSessionsPlayed as pTopAverageDoubleKillsOnChampion, \
        scs6.totalTripleKills/scs6.totalSessionsPlayed as pTopAverageTripleKillsOnChampion, \
        scs6.totalQuadraKills/scs6.totalSessionsPlayed as pTopAverageQuadraKillsOnChampion, \
        scs6.totalPentaKills/scs6.totalSessionsPlayed as pTopAveragePentaKillsOnChampion, \
        scs6.totalUnrealKills/scs6.totalSessionsPlayed as pTopAverageUnrealKillsOnChampion, \
        scs6.totalDeathsPerSession/scs6.totalSessionsPlayed as pTopAverageDeathsPerSessionOnChampion, \
        scs6.totalGoldEarned/scs6.totalSessionsPlayed as pTopAverageGoldEarnedOnChampion, \
        scs6.totalTurretsKilled/scs6.totalSessionsPlayed as pTopAverageTurretsKilledOnChampion, \
        scs6.totalPhysicalDamageDealt/scs6.totalSessionsPlayed as pTopAveragePhysicalDamangeDealtOnChampion, \
        scs6.totalMagicDamageDealt/scs6.totalSessionsPlayed as pTopAverageMagicDamageDealthOnChampion, \
        scs6.totalFirstBlood/scs6.totalSessionsPlayed as pTopAverageFirstBloodOnChampion, \
        scs6.totalAssists/scs6.totalSessionsPlayed as pTopAverageAssits, \
         \
        scs7.totalSessionsPlayed as pJungleTotalSessionsPlayedOnChampion, \
        scs7.totalSessionsLost as pJungleTotalSessionsLostOnChampion, \
        scs7.totalSessionsWon as pJungleTotalSessionsWonOnChampion, \
        scs7.totalSessionsWon/scs7.totalSessionsPlayed as pJungleWinRateOnChampion, \
        scs7.totalChampionKills/scs7.totalSessionsPlayed as pJungleChampionKillsOnChampion, \
        scs7.totalDamageDealt/scs7.totalSessionsPlayed as pJungleAverageDamageDealtOnChampion, \
        scs7.totalDamageTaken/scs7.totalSessionsPlayed as pJungleAverageDamageTakenOnChampion, \
        scs7.totalMinionKills/scs7.totalSessionsPlayed as pJungleAverageMinionKillsOnChampion, \
        scs7.totalDoubleKills/scs7.totalSessionsPlayed as pJungleAverageDoubleKillsOnChampion, \
        scs7.totalTripleKills/scs7.totalSessionsPlayed as pJungleAverageTripleKillsOnChampion, \
        scs7.totalQuadraKills/scs7.totalSessionsPlayed as pJungleAverageQuadraKillsOnChampion, \
        scs7.totalPentaKills/scs7.totalSessionsPlayed as pJungleAveragePentaKillsOnChampion, \
        scs7.totalUnrealKills/scs7.totalSessionsPlayed as pJungleAverageUnrealKillsOnChampion, \
        scs7.totalDeathsPerSession/scs7.totalSessionsPlayed as pJungleAverageDeathsPerSessionOnChampion, \
        scs7.totalGoldEarned/scs7.totalSessionsPlayed as pJungleAverageGoldEarnedOnChampion, \
        scs7.totalTurretsKilled/scs7.totalSessionsPlayed as pJungleAverageTurretsKilledOnChampion, \
        scs7.totalPhysicalDamageDealt/scs7.totalSessionsPlayed as pJungleAveragePhysicalDamangeDealtOnChampion, \
        scs7.totalMagicDamageDealt/scs7.totalSessionsPlayed as pJungleAverageMagicDamageDealthOnChampion, \
        scs7.totalFirstBlood/scs7.totalSessionsPlayed as pJungleAverageFirstBloodOnChampion, \
        scs7.totalAssists/scs7.totalSessionsPlayed as pJungleAverageAssits, \
     \
        scs8.totalSessionsPlayed as pMidTotalSessionsPlayedOnChampion, \
        scs8.totalSessionsLost as pMidTotalSessionsLostOnChampion, \
        scs8.totalSessionsWon as pMidTotalSessionsWonOnChampion, \
        scs8.totalSessionsWon/scs8.totalSessionsPlayed as pMidWinRateOnChampion, \
        scs8.totalChampionKills/scs8.totalSessionsPlayed as pMidChampionKillsOnChampion, \
        scs8.totalDamageDealt/scs8.totalSessionsPlayed as pMidAverageDamageDealtOnChampion, \
        scs8.totalDamageTaken/scs8.totalSessionsPlayed as pMidAverageDamageTakenOnChampion, \
        scs8.totalMinionKills/scs8.totalSessionsPlayed as pMidAverageMinionKillsOnChampion, \
        scs8.totalDoubleKills/scs8.totalSessionsPlayed as pMidAverageDoubleKillsOnChampion, \
        scs8.totalTripleKills/scs8.totalSessionsPlayed as pMidAverageTripleKillsOnChampion, \
        scs8.totalQuadraKills/scs8.totalSessionsPlayed as pMidAverageQuadraKillsOnChampion, \
        scs8.totalPentaKills/scs8.totalSessionsPlayed as pMidAveragePentaKillsOnChampion, \
        scs8.totalUnrealKills/scs8.totalSessionsPlayed as pMidAverageUnrealKillsOnChampion, \
        scs8.totalDeathsPerSession/scs8.totalSessionsPlayed as pMidAverageDeathsPerSessionOnChampion, \
        scs8.totalGoldEarned/scs8.totalSessionsPlayed as pMidAverageGoldEarnedOnChampion, \
        scs8.totalTurretsKilled/scs8.totalSessionsPlayed as pMidAverageTurretsKilledOnChampion, \
        scs8.totalPhysicalDamageDealt/scs8.totalSessionsPlayed as pMidAveragePhysicalDamangeDealtOnChampion, \
        scs8.totalMagicDamageDealt/scs8.totalSessionsPlayed as pMidAverageMagicDamageDealthOnChampion, \
        scs8.totalFirstBlood/scs8.totalSessionsPlayed as pMidAverageFirstBloodOnChampion, \
        scs8.totalAssists/scs8.totalSessionsPlayed as pMidAverageAssits, \
     \
        scs9.totalSessionsPlayed as pBotTotalSessionsPlayedOnChampion, \
        scs9.totalSessionsLost as pBotTotalSessionsLostOnChampion, \
        scs9.totalSessionsWon as pBotTotalSessionsWonOnChampion, \
        scs9.totalSessionsWon/scs9.totalSessionsPlayed as pBotWinRateOnChampion, \
        scs9.totalChampionKills/scs9.totalSessionsPlayed as pBotChampionKillsOnChampion, \
        scs9.totalDamageDealt/scs9.totalSessionsPlayed as pBotAverageDamageDealtOnChampion, \
        scs9.totalDamageTaken/scs9.totalSessionsPlayed as pBotAverageDamageTakenOnChampion, \
        scs9.totalMinionKills/scs9.totalSessionsPlayed as pBotAverageMinionKillsOnChampion, \
        scs9.totalDoubleKills/scs9.totalSessionsPlayed as pBotAverageDoubleKillsOnChampion, \
        scs9.totalTripleKills/scs9.totalSessionsPlayed as pBotAverageTripleKillsOnChampion, \
        scs9.totalQuadraKills/scs9.totalSessionsPlayed as pBotAverageQuadraKillsOnChampion, \
        scs9.totalPentaKills/scs9.totalSessionsPlayed as pBotAveragePentaKillsOnChampion, \
        scs9.totalUnrealKills/scs9.totalSessionsPlayed as pBotAverageUnrealKillsOnChampion, \
        scs9.totalDeathsPerSession/scs9.totalSessionsPlayed as pBotAverageDeathsPerSessionOnChampion, \
        scs9.totalGoldEarned/scs9.totalSessionsPlayed as pBotAverageGoldEarnedOnChampion, \
        scs9.totalTurretsKilled/scs9.totalSessionsPlayed as pBotAverageTurretsKilledOnChampion, \
        scs9.totalPhysicalDamageDealt/scs9.totalSessionsPlayed as pBotAveragePhysicalDamangeDealtOnChampion, \
        scs9.totalMagicDamageDealt/scs9.totalSessionsPlayed as pBotAverageMagicDamageDealthOnChampion, \
        scs9.totalFirstBlood/scs9.totalSessionsPlayed as pBotAverageFirstBloodOnChampion, \
        scs9.totalAssists/scs9.totalSessionsPlayed as pBotAverageAssits, \
     \
        scs10.totalSessionsPlayed as pSupportTotalSessionsPlayedOnChampion, \
        scs10.totalSessionsLost as pSupportTotalSessionsLostOnChampion, \
        scs10.totalSessionsWon as pSupportTotalSessionsWonOnChampion, \
        scs10.totalSessionsWon/scs10.totalSessionsPlayed as pSupportWinRateOnChampion, \
        scs10.totalChampionKills/scs10.totalSessionsPlayed as pSupportChampionKillsOnChampion, \
        scs10.totalDamageDealt/scs10.totalSessionsPlayed as pSupportAverageDamageDealtOnChampion, \
        scs10.totalDamageTaken/scs10.totalSessionsPlayed as pSupportAverageDamageTakenOnChampion, \
        scs10.totalMinionKills/scs10.totalSessionsPlayed as pSupportAverageMinionKillsOnChampion, \
        scs10.totalDoubleKills/scs10.totalSessionsPlayed as pSupportAverageDoubleKillsOnChampion, \
        scs10.totalTripleKills/scs10.totalSessionsPlayed as pSupportAverageTripleKillsOnChampion, \
        scs10.totalQuadraKills/scs10.totalSessionsPlayed as pSupportAverageQuadraKillsOnChampion, \
        scs10.totalPentaKills/scs10.totalSessionsPlayed as pSupportAveragePentaKillsOnChampion, \
        scs10.totalUnrealKills/scs10.totalSessionsPlayed as pSupportAverageUnrealKillsOnChampion, \
        scs10.totalDeathsPerSession/scs10.totalSessionsPlayed as pSupportAverageDeathsPerSessionOnChampion, \
        scs10.totalGoldEarned/scs10.totalSessionsPlayed as pSupportAverageGoldEarnedOnChampion, \
        scs10.totalTurretsKilled/scs10.totalSessionsPlayed as pSupportAverageTurretsKilledOnChampion, \
        scs10.totalPhysicalDamageDealt/scs10.totalSessionsPlayed as pSupportAveragePhysicalDamangeDealtOnChampion, \
        scs10.totalMagicDamageDealt/scs10.totalSessionsPlayed as pSupportAverageMagicDamageDealthOnChampion, \
        scs10.totalFirstBlood/scs10.totalSessionsPlayed as pSupportAverageFirstBloodOnChampion, \
        scs10.totalAssists/scs10.totalSessionsPlayed as pSupportAverageAssits, \
    \
        scs1.totalSessionsPlayed +  \
        scs2.totalSessionsPlayed +  \
        scs3.totalSessionsPlayed +  \
        scs4.totalSessionsPlayed +  \
        scs5.totalSessionsPlayed as bTeamTotalSessionsPlayedOnChamps, \
     \
        scs6.totalSessionsPlayed +  \
        scs7.totalSessionsPlayed +  \
        scs8.totalSessionsPlayed +  \
        scs9.totalSessionsPlayed +  \
        scs10.totalSessionsPlayed as pTeamTotalSessionsPlayedOnChamps, \
         \
        scs1.totalSessionsLost +  \
        scs2.totalSessionsLost +  \
        scs3.totalSessionsLost +  \
        scs4.totalSessionsLost +  \
        scs5.totalSessionsLost as bTeamTotalSessionsLostOnChamps,  \
     \
        scs6.totalSessionsLost +  \
        scs7.totalSessionsLost +  \
        scs8.totalSessionsLost +  \
        scs9.totalSessionsLost +  \
        scs10.totalSessionsLost as pTeamTotalSessionsLostOnChamps, \
         \
        scs1.totalSessionsWon +  \
        scs2.totalSessionsWon +  \
        scs3.totalSessionsWon +  \
        scs4.totalSessionsWon +  \
        scs5.totalSessionsWon as bTeamTotalSessionsWonOnChamps, \
     \
        scs6.totalSessionsWon +  \
        scs7.totalSessionsWon +  \
        scs8.totalSessionsWon +  \
        scs9.totalSessionsWon +  \
        scs10.totalSessionsWon as pTeamTotalSessionsWonOnChamps, \
         \
            scs1.totalChampionKills/scs1.totalSessionsPlayed +  \
        scs2.totalChampionKills/scs2.totalSessionsPlayed +  \
        scs3.totalChampionKills/scs3.totalSessionsPlayed +  \
        scs4.totalChampionKills/scs4.totalSessionsPlayed +  \
        scs5.totalChampionKills/scs5.totalSessionsPlayed as bTeamTotalAverageKills, \
     \
        scs6.totalChampionKills/scs6.totalSessionsPlayed +  \
        scs7.totalChampionKills/scs7.totalSessionsPlayed +  \
        scs8.totalChampionKills/scs8.totalSessionsPlayed +  \
        scs9.totalChampionKills/scs9.totalSessionsPlayed +  \
        scs10.totalChampionKills/scs10.totalSessionsPlayed as pTeamTotalAverageKills, \
         \
        scs1.totalDamageDealt/scs1.totalSessionsPlayed +  \
        scs2.totalDamageDealt/scs2.totalSessionsPlayed +  \
        scs3.totalDamageDealt/scs3.totalSessionsPlayed +  \
        scs4.totalDamageDealt/scs4.totalSessionsPlayed +  \
        scs5.totalDamageDealt/scs5.totalSessionsPlayed as bTeamTotalAverageDamageDealt, \
     \
        scs6.totalDamageDealt/scs6.totalSessionsPlayed +  \
        scs7.totalDamageDealt/scs7.totalSessionsPlayed +  \
        scs8.totalDamageDealt/scs8.totalSessionsPlayed +  \
        scs9.totalDamageDealt/scs9.totalSessionsPlayed +  \
        scs10.totalDamageDealt/scs10.totalSessionsPlayed as pTeamTotalAverageDamageDealt, \
     \
        scs1.totalDamageTaken/scs1.totalSessionsPlayed +  \
        scs2.totalDamageTaken/scs2.totalSessionsPlayed +  \
        scs3.totalDamageTaken/scs3.totalSessionsPlayed +  \
        scs4.totalDamageTaken/scs4.totalSessionsPlayed +  \
        scs5.totalDamageTaken/scs5.totalSessionsPlayed as bTeamTotalAverageDamageTaken, \
     \
        scs6.totalDamageTaken/scs6.totalSessionsPlayed +  \
        scs7.totalDamageTaken/scs7.totalSessionsPlayed +  \
        scs8.totalDamageTaken/scs8.totalSessionsPlayed +  \
        scs9.totalDamageTaken/scs9.totalSessionsPlayed +  \
        scs10.totalDamageTaken/scs10.totalSessionsPlayed as pTeamTotalTeamAverageDamageTaken, \
     \
        scs1.totalMinionKills/scs1.totalSessionsPlayed +  \
        scs2.totalMinionKills/scs2.totalSessionsPlayed +  \
        scs3.totalMinionKills/scs3.totalSessionsPlayed +  \
        scs4.totalMinionKills/scs4.totalSessionsPlayed +  \
        scs5.totalMinionKills/scs5.totalSessionsPlayed as bTeamTotalAverageMinionKills, \
     \
        scs6.totalMinionKills/scs6.totalSessionsPlayed +  \
        scs7.totalMinionKills/scs7.totalSessionsPlayed +  \
        scs8.totalMinionKills/scs8.totalSessionsPlayed +  \
        scs9.totalMinionKills/scs9.totalSessionsPlayed +  \
        scs10.totalMinionKills/scs10.totalSessionsPlayed as pTeamTotalAverageMinionKills, \
     \
        scs1.totalDoubleKills/scs1.totalSessionsPlayed +  \
        scs2.totalDoubleKills/scs2.totalSessionsPlayed +  \
        scs3.totalDoubleKills/scs3.totalSessionsPlayed +  \
        scs4.totalDoubleKills/scs4.totalSessionsPlayed +  \
        scs5.totalDoubleKills/scs5.totalSessionsPlayed as bTeamTotalAverageDoubleKills, \
     \
        scs6.totalDoubleKills/scs6.totalSessionsPlayed +  \
        scs7.totalDoubleKills/scs7.totalSessionsPlayed +  \
        scs8.totalDoubleKills/scs8.totalSessionsPlayed +  \
        scs9.totalDoubleKills/scs9.totalSessionsPlayed +  \
        scs10.totalDoubleKills/scs10.totalSessionsPlayed as pTeamTotalAverageDoubleKills, \
     \
        scs1.totalTripleKills/scs1.totalSessionsPlayed +  \
        scs2.totalTripleKills/scs2.totalSessionsPlayed +  \
        scs3.totalTripleKills/scs3.totalSessionsPlayed +  \
        scs4.totalTripleKills/scs4.totalSessionsPlayed +  \
        scs5.totalTripleKills/scs5.totalSessionsPlayed as bTeamTotalAverageTripleKills, \
        scs6.totalTripleKills/scs6.totalSessionsPlayed +  \
        scs7.totalTripleKills/scs7.totalSessionsPlayed +  \
        scs8.totalTripleKills/scs8.totalSessionsPlayed +  \
        scs9.totalTripleKills/scs9.totalSessionsPlayed +  \
        scs10.totalTripleKills/scs10.totalSessionsPlayed as pTeamTotalAverageTripleKills, \
     \
        scs1.totalQuadraKills/scs1.totalSessionsPlayed +  \
        scs2.totalQuadraKills/scs2.totalSessionsPlayed +  \
        scs3.totalQuadraKills/scs3.totalSessionsPlayed +  \
        scs4.totalQuadraKills/scs4.totalSessionsPlayed +  \
        scs5.totalQuadraKills/scs5.totalSessionsPlayed as bTeamTotalAverageQuadraKills, \
     \
        scs6.totalQuadraKills/scs6.totalSessionsPlayed +  \
        scs7.totalQuadraKills/scs7.totalSessionsPlayed +  \
        scs8.totalQuadraKills/scs8.totalSessionsPlayed +  \
        scs9.totalQuadraKills/scs9.totalSessionsPlayed +  \
        scs10.totalQuadraKills/scs10.totalSessionsPlayed as pTeamTotalAverageQuadraKills, \
     \
        scs1.totalPentaKills/scs1.totalSessionsPlayed +  \
        scs2.totalPentaKills/scs2.totalSessionsPlayed +  \
        scs3.totalPentaKills/scs3.totalSessionsPlayed +  \
        scs4.totalPentaKills/scs4.totalSessionsPlayed +  \
        scs5.totalPentaKills/scs5.totalSessionsPlayed as bTeamTotalAveragePentaKills, \
     \
        scs6.totalPentaKills/scs6.totalSessionsPlayed +  \
        scs7.totalPentaKills/scs7.totalSessionsPlayed +  \
        scs8.totalPentaKills/scs8.totalSessionsPlayed +  \
        scs9.totalPentaKills/scs9.totalSessionsPlayed +  \
        scs10.totalPentaKills/scs10.totalSessionsPlayed as pTeamTotalAveragePentaKills, \
     \
        scs1.totalUnrealKills/scs1.totalSessionsPlayed +  \
        scs2.totalUnrealKills/scs2.totalSessionsPlayed +  \
        scs3.totalUnrealKills/scs3.totalSessionsPlayed +  \
        scs4.totalUnrealKills/scs4.totalSessionsPlayed +  \
        scs5.totalUnrealKills/scs5.totalSessionsPlayed as bTeamTotalAverageUnrealKills, \
     \
        scs6.totalUnrealKills/scs6.totalSessionsPlayed +  \
        scs7.totalUnrealKills/scs7.totalSessionsPlayed +  \
        scs8.totalUnrealKills/scs8.totalSessionsPlayed +  \
        scs9.totalUnrealKills/scs9.totalSessionsPlayed +  \
        scs10.totalUnrealKills/scs10.totalSessionsPlayed as pTeamTotalAverageUnrealKills, \
     \
        scs1.totalDeathsPerSession/scs1.totalSessionsPlayed +  \
        scs2.totalDeathsPerSession/scs2.totalSessionsPlayed +  \
        scs3.totalDeathsPerSession/scs3.totalSessionsPlayed +  \
        scs4.totalDeathsPerSession/scs4.totalSessionsPlayed +  \
        scs5.totalDeathsPerSession/scs5.totalSessionsPlayed as bTeamTotalAverageDeathsPerSession, \
     \
        scs6.totalDeathsPerSession/scs6.totalSessionsPlayed +  \
        scs7.totalDeathsPerSession/scs7.totalSessionsPlayed +  \
        scs8.totalDeathsPerSession/scs8.totalSessionsPlayed +  \
        scs9.totalDeathsPerSession/scs9.totalSessionsPlayed +  \
        scs10.totalDeathsPerSession/scs10.totalSessionsPlayed as pTeamTotalAverageDeahtsPerSession, \
     \
        scs1.totalGoldEarned/scs1.totalSessionsPlayed +  \
        scs2.totalGoldEarned/scs2.totalSessionsPlayed +  \
        scs3.totalGoldEarned/scs3.totalSessionsPlayed +  \
        scs4.totalGoldEarned/scs4.totalSessionsPlayed +  \
        scs5.totalGoldEarned/scs5.totalSessionsPlayed as bTeamTotalAverageGoldEarned, \
     \
        scs6.totalGoldEarned/scs6.totalSessionsPlayed +  \
        scs7.totalGoldEarned/scs7.totalSessionsPlayed +  \
        scs8.totalGoldEarned/scs8.totalSessionsPlayed +  \
        scs9.totalGoldEarned/scs9.totalSessionsPlayed +  \
        scs10.totalGoldEarned/scs10.totalSessionsPlayed as pTeamTotalAverageGoldEarned, \
     \
        scs1.totalTurretsKilled/scs1.totalSessionsPlayed +  \
        scs2.totalTurretsKilled/scs2.totalSessionsPlayed +  \
        scs3.totalTurretsKilled/scs3.totalSessionsPlayed +  \
        scs4.totalTurretsKilled/scs4.totalSessionsPlayed +  \
        scs5.totalTurretsKilled/scs5.totalSessionsPlayed as bTeamTotalAverageTurretsKilled, \
     \
        scs6.totalTurretsKilled/scs6.totalSessionsPlayed +  \
        scs7.totalTurretsKilled/scs7.totalSessionsPlayed +  \
        scs8.totalTurretsKilled/scs8.totalSessionsPlayed +  \
        scs9.totalTurretsKilled/scs9.totalSessionsPlayed +  \
        scs10.totalTurretsKilled/scs10.totalSessionsPlayed as pTeamTotalAverageTurretsKilled, \
     \
        scs1.totalPhysicalDamageDealt/scs1.totalSessionsPlayed +  \
        scs2.totalPhysicalDamageDealt/scs2.totalSessionsPlayed +  \
        scs3.totalPhysicalDamageDealt/scs3.totalSessionsPlayed +  \
        scs4.totalPhysicalDamageDealt/scs4.totalSessionsPlayed +  \
        scs5.totalPhysicalDamageDealt/scs5.totalSessionsPlayed as bTeamTotalAverageTotalPhysicalDamageDealt, \
     \
        scs6.totalPhysicalDamageDealt/scs6.totalSessionsPlayed +  \
        scs7.totalPhysicalDamageDealt/scs7.totalSessionsPlayed +  \
        scs8.totalPhysicalDamageDealt/scs8.totalSessionsPlayed +  \
        scs9.totalPhysicalDamageDealt/scs9.totalSessionsPlayed +  \
        scs10.totalPhysicalDamageDealt/scs10.totalSessionsPlayed as pTeamTotalAverageTotalPhysicalDamageDealt, \
     \
        scs1.totalMagicDamageDealt/scs1.totalSessionsPlayed +  \
        scs2.totalMagicDamageDealt/scs2.totalSessionsPlayed +  \
        scs3.totalMagicDamageDealt/scs3.totalSessionsPlayed +  \
        scs4.totalMagicDamageDealt/scs4.totalSessionsPlayed +  \
        scs5.totalMagicDamageDealt/scs5.totalSessionsPlayed as bTeamTotalAverageTotalMagicDamageDealt, \
     \
        scs6.totalMagicDamageDealt/scs6.totalSessionsPlayed +  \
        scs7.totalMagicDamageDealt/scs7.totalSessionsPlayed +  \
        scs8.totalMagicDamageDealt/scs8.totalSessionsPlayed +  \
        scs9.totalMagicDamageDealt/scs9.totalSessionsPlayed +  \
        scs10.totalMagicDamageDealt/scs10.totalSessionsPlayed as pTeamTotalAverageTotalMagicDamageDealt, \
     \
        scs1.totalFirstBlood/scs1.totalSessionsPlayed +  \
        scs2.totalFirstBlood/scs2.totalSessionsPlayed +  \
        scs3.totalFirstBlood/scs3.totalSessionsPlayed +  \
        scs4.totalFirstBlood/scs4.totalSessionsPlayed +  \
        scs5.totalFirstBlood/scs5.totalSessionsPlayed as bTeamTotalAverageFirstBlood, \
     \
        scs6.totalFirstBlood/scs6.totalSessionsPlayed +  \
        scs7.totalFirstBlood/scs7.totalSessionsPlayed +  \
        scs8.totalFirstBlood/scs8.totalSessionsPlayed +  \
        scs9.totalFirstBlood/scs9.totalSessionsPlayed +  \
        scs10.totalFirstBlood/scs10.totalSessionsPlayed as pTeamTotalAverageFirstBlood, \
     \
        scs1.totalAssists/scs1.totalSessionsPlayed +  \
        scs2.totalAssists/scs2.totalSessionsPlayed +  \
        scs3.totalAssists/scs3.totalSessionsPlayed +  \
        scs4.totalAssists/scs4.totalSessionsPlayed +  \
        scs5.totalAssists/scs5.totalSessionsPlayed as bTeamTotalAverageAssists, \
     \
        scs6.totalAssists/scs6.totalSessionsPlayed +  \
        scs7.totalAssists/scs7.totalSessionsPlayed +  \
        scs8.totalAssists/scs8.totalSessionsPlayed +  \
        scs9.totalAssists/scs9.totalSessionsPlayed +  \
        scs10.totalAssists/scs10.totalSessionsPlayed as pTeamTotalAverageAssists,  \
         \
    mr.bWin \
    FROM matchResults mr \
    INNER JOIN globalChampionAverages as gca1 on gca1.champId=mr.bTopChampId and gca1.role='Top' \
    INNER JOIN globalChampionAverages as gca2 on gca2.champId=mr.bJungleChampId and gca2.role='Jungle' \
    INNER JOIN globalChampionAverages as gca3 on gca3.champId=mr.bMidChampId and gca3.role='Middle' \
    INNER JOIN globalChampionAverages as gca4 on gca4.champId=mr.bBotChampId and gca4.role='ADC' \
    INNER JOIN globalChampionAverages as gca5 on gca5.champId=mr.bSupportChampId and gca5.role='Support' \
    INNER JOIN globalChampionAverages as gca6 on gca6.champId=mr.pTopChampId and gca6.role='Top' \
    INNER JOIN globalChampionAverages as gca7 on gca7.champId=mr.pJungleChampId and gca7.role='Jungle' \
    INNER JOIN globalChampionAverages as gca8 on gca8.champId=mr.pMidChampId and gca8.role='Middle' \
    INNER JOIN globalChampionAverages as gca9 on gca9.champId=mr.pBotChampId and gca9.role='ADC' \
    INNER JOIN globalChampionAverages as gca10 on gca10.champId=mr.pSupportChampId and gca10.role='Support' \
    INNER JOIN summonerChampionStats as scs1 on scs1.summonerId=mr.bTopId and scs1.championId=mr.bTopChampId \
    INNER JOIN summonerChampionStats as scs2 on scs2.summonerId=mr.bJungleId and scs2.championId=mr.bJungleChampId \
    INNER JOIN summonerChampionStats as scs3 on scs3.summonerId=mr.bMidId and scs3.championId=mr.bMidChampId \
    INNER JOIN summonerChampionStats as scs4 on scs4.summonerId=mr.bBotId and scs4.championId=mr.bBotChampId \
    INNER JOIN summonerChampionStats as scs5 on scs5.summonerId=mr.bSupportId and scs5.championId=mr.bSupportChampId \
    INNER JOIN summonerChampionStats as scs6 on scs6.summonerId=mr.pTopId and scs6.championId=mr.pTopChampId \
    INNER JOIN summonerChampionStats as scs7 on scs7.summonerId=mr.pJungleId and scs7.championId=mr.pJungleChampId \
    INNER JOIN summonerChampionStats as scs8 on scs8.summonerId=mr.pMidId and scs8.championId=mr.pMidChampId \
    INNER JOIN summonerChampionStats as scs9 on scs9.summonerId=mr.pBotId and scs9.championId=mr.pBotChampId \
    INNER JOIN summonerChampionStats as scs10 on scs10.summonerId=mr.pSupportId and scs10.championId=mr.pSupportChampId; \
    " \

engine = create_engine('mysql+mysqlconnector://root:password@localhost:3306/loldata', echo=False)

rawDataframe = pd.read_sql(DATAFRAME_SQL_QUERY, engine.raw_connection()).convert_objects(convert_numeric=True)
xDataframe = rawDataframe.drop(['bWin'], 1)
yDataframe = rawDataframe['bWin']

#normalize data for X Data
mu = np.mean(xDataframe, axis=0)
sigma = np.std(xDataframe, axis=0)
xDataframe = (xDataframe-mu)/sigma

#drop all shitty columns
xDataframe = xDataframe.dropna(axis=1)

dataframe = xDataframe.join(yDataframe)

#get 60% train, 20% test, 20% cross validation
train, intermediate = train_test_split(dataframe, test_size = 0.4)
test, validation = train_test_split(intermediate, test_size = 0.5)

def getFullDataframe():
    return dataframe

def getTrainingDataframe():
    return train

def getTestDataframe():
    return test

def getValidationDataframe():
    return validation

if __name__ == '__main__':
    df = pd.read_sql(DATAFRAME_SQL_QUERY, engine.raw_connection())
    print (df.head())




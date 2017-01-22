import migration

#migration.purge();
migration.defineGlobalChampionAverages()
migration.defineSummonerChampionStats()
migration.defineApiQueue()
migration.defineSummoners()
migration.defineMatchResults()
migration.closeDb()
print ("End of migrations")

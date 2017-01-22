import summonerRepository
import summonerDataRepository


def getSummonerChampionStats():
    missingSummonersList = summonerRepository.getAllMissingMatchResultSummonerIds()

    print len(missingSummonersList)

    for summonerId in [i[0] for i in missingSummonersList]:
        print summonerId
        summonerDataRepository.updateSummonerData(summonerId)

if __name__ == '__main__':
    getSummonerChampionStats()


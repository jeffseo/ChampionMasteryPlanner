import requests
import json
import RiotConstants as Consts
import imp
masteryPointFormula = imp.load_source("masteryPointFormula", "lolserver/api/masteryPointFormula.py")

class ChampionInfo(object):
    def __init__(self):
        self.championName = None;
        self.championLevel = None;
        self.championPoints = None;
        self.pointsUntilNextLevel = None;
        self.pointsSinceLastLevel = None;
        self.championIcon = None;
        self.gamesNeeded = None;

    def setUnplayedInfo(self, championName):
        self.championName = championName
        self.championLevel = 1
        self.championPoints = 0
        self.pointsUntilNextLevel = 1800
        self.championIcon = None
        self.gamesNeeded = 30


class RiotAPI(object):

    def __init__(self, api_key, region=Consts.ENDPOINTS['NA']['region']):
        self.api_key = api_key
        self.region = region

    def _request(self, api_url, params={}, isGlobal=False):
        args = {'api_key': self.api_key}
        for key, value in params.items():
            if key not in args:
                args[key] = value
        if isGlobal:
            getString = Consts.URL['base'].format(proxy=Consts.ENDPOINTS['Global']['region'],url=api_url)
        else:
            getString = Consts.URL['base'].format(proxy=self.region,url=api_url)
        response = requests.get(getString,params=args)
        if response.status_code == 200:
            return response.json()
        else:
            return None #TODO: think of what to do in these scenarios

    def getSummonerByName(self, name):
        api_url = Consts.URL['summoner_by_name'].format(region=self.region,
                                                        version=Consts.API_VERSIONS['summoner'],
                                                        names=name)
        return self._request(api_url)

    def getChampionMasteryList(self, summonerId, limit=None):
        championMasteryList = []
        if not limit:
            api_url = Consts.URL['all_champion_mastery'].format(platformId=Consts.ENDPOINTS[self.region]['platform'],
                                                                playerId=summonerId)
        else:
            api_url = Consts.URL['top_champion_mastery'].format(platformId=Consts.ENDPOINTS[self.region]['platform'],
                                                                playerId=summonerId,
                                                                count=limit)
        masteryJson = self._request(api_url)
        for champion in masteryJson:
            currentChampionInfo = ChampionInfo()
            currentChampionInfo.championName = self.getChampionNameById(champion['championId'])
            currentChampionInfo.championLevel = champion['championLevel'] 
            currentChampionInfo.championPoints = champion['championPoints'];
            currentChampionInfo.pointsUntilNextLevel = champion['championPointsUntilNextLevel'];
            currentChampionInfo.pointsSinceLastLevel = champion['championPointsSinceLastLevel'];
            currentChampionInfo.championIcon = self.getChampionImageSource(self.getChampionKey(champion['championId']))
            # Assuming 50% win rate.
            currentChampionInfo.gamesNeeded = masteryPointFormula.pointsRequired(float(champion['championPoints']), 21600, 0.5)

            championMasteryList.append(currentChampionInfo)
        return championMasteryList

# {
#    "championPoints": 29218,
#    "playerId": 29484755,
#    "championPointsUntilNextLevel": 0,
#    "chestGranted": false,
#    "championLevel": 5,
#    "championId": 157,
#    "championPointsSinceLastLevel": 7618,
#    "lastPlayTime": 1462081320000
# }
    def getChampionMastery(self, playerId, championId):
        api_url = Consts.URL['single_champion_mastery'].format( platformId=Consts.ENDPOINTS[self.region]['platform'],
                                                                playerId=playerId,
                                                                championId=championId)
        championJson = self._request(api_url)
        
        champion = ChampionInfo()
        if not championJson:
            champion.setUnplayedInfo(self.getChampionNameById(championId))
            champion.championIcon = self.getChampionImageSource(self.getChampionKey(championId))
            return champion
        champion.championName = self.getChampionNameById(championId)
        champion.championLevel = championJson['championLevel'] 
        champion.championPoints = championJson['championPoints'];
        champion.pointsUntilNextLevel = championJson['championPointsUntilNextLevel'];
        champion.pointsSinceLastLevel = championJson['championPointsSinceLastLevel'];
        champion.championIcon = self.getChampionImageSource(self.getChampionKey(championJson['championId']))
        champion.gamesNeeded = masteryPointFormula.pointsRequired(float(champion.championPoints), 21600, 0.5)
        return champion

    #local for now
    def isChampionNameValid(self, championName):
        with open('static-champion-data.json', 'r') as staticChampionData:    
            data = (json.load(staticChampionData))['data']
            for k,v in data.items():
                if v['name'].lower() == championName.lower():
                    return True
        return False

    def getChampionImageSource(self, championKey):
        version = self.getLatestVersion()
        return 'http://ddragon.leagueoflegends.com/cdn/{version}/img/champion/{championKey}.png'.format(version=version,
                                                                                                        championKey=championKey)

    def getLatestVersion(self):
        api_url = Consts.URL['league_version'].format(region=self.region.lower(),version =Consts.API_VERSIONS['static-data'])
        versionJson = self._request(api_url, isGlobal=True)
        return versionJson[0]

    #local for now
    def getChampionKey(self, championId, version=None):
        with open('static-champion-data.json') as staticChampionData:    
            data = (json.load(staticChampionData))['data']
            return data[str(championId)]['key']

    #local for now
    def getChampionId(self, championName):
        with open('static-champion-data.json', 'r') as staticChampionData:    
            data = (json.load(staticChampionData))['data']
            for k,v in data.items():
                if v['name'].lower() == championName.lower():
                    return v['id']

    def getChampionNameById(self,championId, region=None):
        if region is None: #static file to consume less time
            with open('static-champion-data.json', 'r') as staticChampionData:    
                data = (json.load(staticChampionData))['data']
                return data[str(championId)]['name']
        else:
            api_url = Consts.URL['champion_by_id'].format(region=self.region.lower(),
                                                        version=Consts.API_VERSIONS['static-data'],
                                                        id=championId)
            championJson = self._request(api_url, isGlobal=True)
            print championJson
            return championJson['name']




        

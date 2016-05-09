from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render_to_response
from django.template import RequestContext
import RiotConstants
from RiotAPI import RiotAPI
import masteryPointFormula
import time
# Create your views here.

def index(request):
    return render(request,'templates/main.html')

def parseRecentMatches(matchesJson):
        gamesByDate = {}
        for game in matchesJson:
            if game['subType'] in RiotConstants.VALID_GAME_MODES:
                dateOfGame = game['createDate']
                dateStamp = time.ctime(int(dateOfGame) / 1000)
                parsedDateStamp = dateStamp[4:10] + ", " + dateStamp[20:]                
                if parsedDateStamp in gamesByDate:
                    # Formula used to get estimate of Champion Mastery Point gain.
                    gamesByDate[parsedDateStamp] += masteryPointFormula.pointsForGame((float(game['stats']['timePlayed']) / 60), bool(game['stats']['win']))
                else:
                    gamesByDate[parsedDateStamp] = masteryPointFormula.pointsForGame((float(game['stats']['timePlayed']) / 60), bool(game['stats']['win']))
        prepDataForJS = []
        dateLabels = []
        pointsGained = []
        for day in gamesByDate:
            dateLabels.append(day) 
            
        # dicts do not preserve order. The code below accounts for this.
        dateLabels.sort()
        for date in dateLabels:
            pointsGained.append(gamesByDate[date])
        prepDataForJS.append(dateLabels)
        prepDataForJS.append(pointsGained)
        return prepDataForJS        

def summoner(request):
    context = {}
    summonerName = request.GET.get('summonerName', None)
    region = request.GET.get('region', None)
    context['errorFlag'] = "false"
    if not summonerName or not region:
        #TODO: ADD ERROR PAGE(?)
        print 'error'
        return render(request, 'error')
    else:
        api = RiotAPI(RiotConstants.API_KEY, region)
        # Catches TypeError when user enters invalid summoner name.
        try:
            context['summonerName'] = summonerName
            context['region'] = region
            summonerName = summonerName.replace(' ','')
            summonerId = api.getSummonerByName(summonerName)[summonerName.lower()]['id']
            championList = api.getChampionMasteryList(summonerId,10)
    
            context['championList'] = championList
            # creating a list of champions for dropdown in champion search bar.
            championListOrdered = []
    
            for k,v in api.getChampionListByName().items():
                championListOrdered.append([v['name'],v['key']])
            championListOrdered.sort()
            context['orderedChampionList'] = championListOrdered
            # recentMatchesData returns a list with two elements. The first is a 
            # list of the labels for the graphs (days) and the second is a list
            # of champion point values corresponding to the day labels.
            recentMatchesData = api.getRecentMatches(summonerId)
            recentMatchesDataParsed = parseRecentMatches(recentMatchesData)
            context['graphLabels'] = recentMatchesDataParsed[0]
            context['graphData'] = recentMatchesDataParsed[1]
            return render(request,'templates/summoner.html', context)          
        except TypeError:
            print("TypeError")
            context['errorFlag'] = "true"
            context['summonerName'] = summonerName
            return render(request, 'templates/main.html', context)        

def champion(request):
    context = {}
    championKey = request.GET.get('championName', None)
    summonerName = request.GET.get('summonerName', None)
    region = request.GET.get('region', None)
    if not summonerName or not region or not championKey:
        #TODO: ADD ERROR PAGE(?)
        print 'error'
        return render(request, 'error')
    else:
        
        api = RiotAPI(RiotConstants.API_KEY, region)
        championName = api.getChampionNameByKey(championKey)
        context['summonerName'] = summonerName
        summonerName = summonerName.replace(' ','')
        summonerId = api.getSummonerByName(summonerName)[summonerName.lower()]['id']
        championId = api.getChampionId(championName)
        context['championMasteryFor5'] = RiotConstants.MASTERY_POINTS[5]
        context['championName'] = championName
        context['region'] = region
        context['champion'] = api.getChampionMastery(summonerId, championId)
        context['championImage'] = api.getChampionBackgroundImage(championKey)

        # creating a list of champions for dropdown in champion search bar.
        championListOrdered = []
        for k,v in api.getChampionListByName().items():
            championListOrdered.append([v['name'],v['key']])
        championListOrdered.sort()
        context['orderedChampionList'] = championListOrdered
        
        return render(request,'templates/champion.html', context)    

def info(request):
    return render(request, 'templates/info.html')

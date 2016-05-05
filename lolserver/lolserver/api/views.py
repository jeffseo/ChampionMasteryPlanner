from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render_to_response
from django.template import RequestContext
import RiotConstants
from RiotAPI import RiotAPI
# Create your views here.

def index(request):
    return render(request,'templates/main.html')

def summoner(request):
    context = {}
    summonerName = request.GET.get('summonerName', None)
    region = request.GET.get('region', None)
    if not summonerName or not region:
        #TODO: ADD ERROR PAGE(?)
        print 'error'
        return render(request, 'error')
    else:
        api = RiotAPI(RiotConstants.API_KEY, region)
        summonerId = api.getSummonerByName(summonerName)[summonerName]['id']
        championList = api.getChampionMasteryList(summonerId)
        context['summonerName'] = summonerName
        context['region'] = region
        context['championList'] = championList
        return render(request,'templates/summoner.html', context)

def champion(request):
    context = {}
    championName = request.GET.get('championName', None)
    summonerName = request.GET.get('summonerName', None)
    region = request.GET.get('region', None)
    if not summonerName or not region or not championName:
        #TODO: ADD ERROR PAGE(?)
        print 'error'
        return render(request, 'error')
    else:
        api = RiotAPI(RiotConstants.API_KEY, region)
        summonerId = api.getSummonerByName(summonerName)[summonerName]['id']
        championMastery = api.getChampionMastery(summonerId, api.getChampionId(championName))
        context['championName'] = championName
        context['summonerName'] = summonerName
        context['region'] = region
        context['champion'] = api.getChampionMastery(summonerId, api.getChampionId(championName))

        return render(request,'templates/champion.html', context)    


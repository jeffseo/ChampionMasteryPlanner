import time
import masteryPointFormula
import RiotConstants

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
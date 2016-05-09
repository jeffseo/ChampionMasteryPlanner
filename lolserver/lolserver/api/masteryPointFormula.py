import math

def gamesRequired(currentPoints, desiredPoints, winRate):
    """ 
    Assume each game is 35 minutes long. 
    Given the user's current champion mastery points (currentPoints),
    their desired mastery points for a champion (desiredPoints),
    and a winrate, determine the number of games required (on average) to reach
    the desired champion mastery point goal.
    """
    
    # pointsForWin and pointsForLoss assumes 35 minute games. Numbers are 
    # determined using a regression model (see the Excel file).
    pointsForWin = 1256.58792651
    pointsForLoss = 222.266550523


    neededPoints = desiredPoints - currentPoints
    if neededPoints <= 0:
        return 0
    else:
        avgPointPerGame = winRate * pointsForWin + (1 - winRate) * pointsForLoss
        return int(math.ceil(neededPoints / avgPointPerGame))
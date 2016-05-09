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

def pointsForGame(duration, win):
    """
    win is a boolean representing if the game in question is a victory (True)
    or less (False). The float duration represents the duration of the game
    in question (in minutes).
    
    The int return value represents our estimate of the number of Champion
    Mastery Points gained for the game in question. Our estimate in seen in the
    Excel file named ChampMasteryData.
    """
    
    if win:
        return int((duration + 12.876) / 0.0381)
    else:
        return int((duration + 3.2743) / 0.1722)
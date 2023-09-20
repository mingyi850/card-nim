import time
import pprint 

def hashableSet(original):
    return ','.join([str(i) for i in sorted(list(original))])

def toSet(hashed):
    if not hashed:
        return set()
    return set([int(x) for x in hashed.split(',')])

def addToMatrix(stones, yours, opps, toAdd, matrix, turn):
    #print("adding for stones", stones, "with hand", yours, "With opponent hand", opps, "with result", toAdd)
    yourHash = hashableSet(yours)
    oppHash = hashableSet(opps)
    if stones not in matrix:
        matrix[stones] = dict()
    if yourHash not in matrix[stones]:
        matrix[stones][yourHash] = dict()
    if oppHash not in matrix[stones][yourHash]:
        matrix[stones][yourHash][oppHash] = dict()
    matrix[stones][yourHash][oppHash][turn] = toAdd

#Check if position is winning for you
def isWin(hand, stones, matrix, oppHand, turn):
    #print("Checking win with hand", hand, "stones", stones, "oppHand", oppHand)
    hashableHand = hashableSet(hand)
    hashableOppHand = hashableSet(oppHand)
    if stones in matrix and hashableHand in matrix[stones] and hashableOppHand in matrix[stones][hashableHand] and turn in matrix[stones][hashableHand][hashableOppHand]:
        return matrix[stones][hashableHand][hashableOppHand][turn]
    playerHand = set()
    otherPlayerHand = set()
    if turn:
        playerHand = hand
        otherPlayerHand = oppHand
    else:
        playerHand = oppHand
        otherPlayerHand = hand
    winningSet = set()
    if stones in playerHand:
        return {stones}
    elif not playerHand or stones < min(playerHand):
        return {}
    else:
        for card in (toPlay for toPlay in playerHand if toPlay <= stones):
            newHand = set(playerHand)
            newHand.discard(card)
            target = set()
            targetStones = stones - card
            newHand = reduceHand(targetStones, newHand)
            newOtherHand = reduceHand(targetStones, otherPlayerHand)
            if turn:
                #print("Stones:", targetStones, "Player: ", newHand, "Other:", newOtherHand)
                target = isWin(newHand, targetStones, matrix, newOtherHand, not turn) #matrix[stones - card][hashableSet(newHand)][hashableSet(newOtherHand)]
            else:
                target = isWin(newOtherHand, targetStones, matrix, newHand, not turn)#matrix[stones - card][hashableSet(newOtherHand)][hashableSet(newHand)]
            if not target:
                return {card} 
            else:
                continue
    return winningSet

def checkDone(matrix, stones, currentHand, currentOppHand, starting):
    hashableHand = hashableSet(currentHand)
    hashableOppHand = hashableSet(currentOppHand)
    if stones in matrix:
        if hashableHand in matrix[stones]:
            if hashableOppHand in matrix[stones][hashableHand]:
                if starting in matrix[stones][hashableHand][hashableOppHand]:
                    return True
    return False

def reduceHand(stones, hand):
    return {card for card in hand if card <= stones}

def handCondition(turn, myHand, oppHand):
    firstHand = myHand
    secondHand = oppHand
    return (turn and len(secondHand) - len(firstHand) in {2,1}) or (not turn and len(firstHand) == len(secondHand))
    
def checkNewCard(playerHandSet, otherPlayerHandSet, stones, maxStones, matrix, turn, newCard):
    newPlayerHand = playerHandSet.copy()
    newPlayerHand.add(newCard)
    newPlayerHand = reduceHand(stones, newPlayerHand)
    if turn:
        if sum(newPlayerHand) + sum(otherPlayerHandSet) >= stones:
            addToMatrix(stones, newPlayerHand, otherPlayerHandSet, isWin(newPlayerHand, stones, matrix, otherPlayerHandSet, turn), matrix, turn)
        else:
            addToMatrix(stones, newPlayerHand, otherPlayerHandSet, set(), matrix, turn)
        if sum(newPlayerHand) + sum(otherPlayerHandSet) >= stones + newCard and stones + newCard < maxStones:
            addToMatrix(stones + newCard, newPlayerHand, otherPlayerHandSet, isWin(newPlayerHand, stones + newCard, matrix, otherPlayerHandSet, turn), matrix, turn)
    else:
        if sum(newPlayerHand) + sum(otherPlayerHandSet) >= stones:
            addToMatrix(stones, otherPlayerHandSet, newPlayerHand, isWin(otherPlayerHandSet, stones, matrix, newPlayerHand, turn), matrix, turn)
        else:
            addToMatrix(stones, otherPlayerHandSet, newPlayerHand, set(), matrix, turn)
        if sum(newPlayerHand) + sum(otherPlayerHandSet) >= stones + newCard and stones + newCard < maxStones:
            addToMatrix(stones + newCard, otherPlayerHandSet, newPlayerHand, isWin(otherPlayerHandSet, stones + newCard, matrix, newPlayerHand, turn), matrix, turn)

def getMatrix(maxStones, cards, currentHand, currentOppHand, starting):
    #Initialise matrix
    matrix = dict()
    for i in range(maxStones + 1):
        matrix[i] = dict()
        matrix[i][""] = dict() 
        matrix[i][""][""] = dict()
        matrix[i][""][""][True] = {}
        matrix[i][""][""][False] = {1}

    
    reducedHand = reduceHand(maxStones, currentHand)
    reducedOppHand = reduceHand(maxStones, currentOppHand)
    # Start base case
    turn = not starting
    while not checkDone(matrix, maxStones, reducedHand, reducedOppHand, starting):
    #for i in range(10):
        for stones in range(0, maxStones + 1):
            #print("STONES: ", stones)
            yourCurrentHands = matrix[stones].copy()
            for yourHand in yourCurrentHands:
                handSet = toSet(yourHand)
                oppHands = yourCurrentHands[yourHand].copy()
                for oppHand in [hand for hand in oppHands if handCondition(turn, yourHand, hand)]:
                    oppHandSet = toSet(oppHand)
                    #print("Opp hand: ", oppHand, "My hand: ", yourHand)
                    playerHandSet = set()
                    otherPlayerHandSet = set()
                    if turn:
                        #print("My turn, with hands: ", handSet, oppHandSet)
                        playerHandSet = handSet
                        playerCurrentHand = currentHand
                        otherPlayerHandSet = oppHandSet
                    else:
                        #print("Opp turn, with hands: ", handSet, oppHandSet)
                        playerHandSet = oppHandSet
                        playerCurrentHand = currentOppHand
                        otherPlayerHandSet = handSet
                    for newCard in [x for x in playerCurrentHand if x not in playerHandSet]: #only build cards in hand
                        checkNewCard(playerHandSet, otherPlayerHandSet, stones, maxStones, matrix, turn, newCard)
        turn = not turn
    print("Solution: ", matrix[maxStones][hashableSet(reducedHand)][hashableSet(reducedOppHand)][True])
    return matrix

startTime = time.time()
matrix = getMatrix(25, 15, set([1,2,3,4,5,6,7,8,9,10]), set([1,2,3,4,5,6,7,8,9,10]), True) # 8 cards takes 44 seconds
#pprint.pprint(matrix)
print("--- Program finished in %s seconds ---" % (time.time() - startTime))



"""
s = 23, k = 7:  DP Starts first 
DP plays 7 (16)
Opp plays 7 (9)
DP play 1 (8)
Opp plays 1 (7)
DP plays 6 (1)
Opp loses

s = 23, k = 7:  DP Starts first 
Opp plays 5 (18)
DP plays 5 (13)
Opp plays 4 (9)
DP plays 4 (5)
Opp plays 1 (4)
Dp plays 3 (1)
Opp loses 

If i play 5,
getMatrix
"""





        



            
                
    

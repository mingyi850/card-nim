import time

def hashableSet(original):
    return ','.join([str(i) for i in sorted(list(original))])

def toSet(hashed):
    if not hashed:
        return set()
    return set([int(x) for x in hashed.split(',')])

def addToMatrix(stones, yours, opps, toAdd, matrix):
    #print("adding for stones", stones, "with hand", yours, "With opponent hand", opps, "with result", toAdd)
    yourHash = hashableSet(yours)
    oppHash = hashableSet(opps)
    if stones not in matrix:
        matrix[stones] = dict()
    if yourHash not in matrix[stones]:
        matrix[stones][yourHash] = dict()
    matrix[stones][yourHash][oppHash] = toAdd

#Check if position is winning for you
def isWin(hand, stones, matrix, oppHand, turn):
    #print("Checking win with hand", hand, "stones", stones, "oppHand", oppHand)
    hashableHand = hashableSet(hand)
    hashableOppHand = hashableSet(oppHand)
    if stones in matrix and hashableHand in matrix[stones] and hashableOppHand in matrix[stones][hashableHand]:
        return matrix[stones][hashableHand][hashableOppHand]
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
            if turn:
                #print("Stones:", targetStones, "Player: ", newHand, "Other:", newOtherHand)
                target = isWin(newHand, targetStones, matrix, otherPlayerHand, not turn) #matrix[stones - card][hashableSet(newHand)][hashableSet(newOtherHand)]
            else:
                target = isWin(otherPlayerHand, targetStones, matrix, newHand, not turn)#matrix[stones - card][hashableSet(newOtherHand)][hashableSet(newHand)]
            if not target:
                return {card} 
            else:
                continue
    return winningSet

def checkDone(matrix, stones, currentHand, currentOppHand):
    hashableHand = hashableSet(currentHand)
    hashableOppHand = hashableSet(currentOppHand)
    if stones in matrix:
        if hashableHand in matrix[stones]:
            if hashableOppHand in matrix[stones][hashableHand]:
                return True
    return False

def reduceHand(stones, hand):
    return {card for card in hand if card <= stones}

def handCondition(turn, myHand, oppHand):
    return (turn and len(oppHand) - len(myHand) in {2,1}) or (not turn and len(myHand) == len(oppHand))
    
def checkNewCard(playerHandSet, otherPlayerHandSet, stones, maxStones, matrix, turn, newCard):
    newPlayerHand = playerHandSet.copy()
    newPlayerHand.add(newCard)
    if turn:
        if sum(newPlayerHand) + sum(otherPlayerHandSet) >= stones:
            addToMatrix(stones, newPlayerHand, otherPlayerHandSet, isWin(newPlayerHand, stones, matrix, otherPlayerHandSet, turn), matrix)
        else:
            addToMatrix(stones, newPlayerHand, otherPlayerHandSet, set(), matrix)
        if sum(newPlayerHand) + sum(otherPlayerHandSet) >= stones + newCard and stones + newCard < maxStones:
            addToMatrix(stones + newCard, newPlayerHand, otherPlayerHandSet, isWin(newPlayerHand, stones + newCard, matrix, otherPlayerHandSet, turn), matrix)
    else:
        if sum(newPlayerHand) + sum(otherPlayerHandSet) >= stones:
            addToMatrix(stones, otherPlayerHandSet, newPlayerHand, isWin(otherPlayerHandSet, stones, matrix, newPlayerHand, turn), matrix)
        else:
            addToMatrix(stones, otherPlayerHandSet, newPlayerHand, set(), matrix)
        if sum(newPlayerHand) + sum(otherPlayerHandSet) >= stones + newCard and stones + newCard < maxStones:
            addToMatrix(stones + newCard, otherPlayerHandSet, newPlayerHand, isWin(otherPlayerHandSet, stones + newCard, matrix, newPlayerHand, turn), matrix)

def getMatrix(maxStones, cards, currentHand, currentOppHand, starting):
    #Initialise matrix
    matrix = dict()
    for i in range(maxStones + 1):
        matrix[i] = dict()
        matrix[i][""] = dict() 
        matrix[i][""][""] = set()
    # Start base case
    turn = not starting
    while not checkDone(matrix, maxStones, currentHand, currentOppHand):
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
    print("Solution: ", matrix[maxStones][hashableSet(currentHand)][hashableSet(currentOppHand)])
    return matrix

startTime = time.time()
matrix = getMatrix(20, 7, set([1,2,3,4,5,6,7]), set([1,2,3,4,5,6,7]), True) # 8 cards takes 44 seconds
print("--- Program finished in %s seconds ---" % (time.time() - startTime))



"""
Solution: 5, 6 or 7

If i play 5,
getMatrix
"""





        



            
                
    

import multiprocessing
import pprint
import time

hashUsed = 0
nonHashUse = 0

def hashableSet(original: set[int]):
    return ','.join([str(i) for i in sorted(list(original))])

def toSet(hashed: str) -> set[int]:
    if not hashed:
        return set()
    return set([int(x) for x in hashed.split(',')])

def addToMatrix(stones: int, yours: set[int], opps: set[int], toAdd: set[int], matrix):
    #print("adding for stones", stones, "with hand", yours, "With opponent hand", opps, "with result", toAdd)
    yourHash = hashableSet(yours)
    oppHash = hashableSet(opps)
    if stones not in matrix:
        matrix[stones] = dict()
    if yourHash not in matrix[stones]:
        matrix[stones][yourHash] = dict()
    matrix[stones][yourHash][oppHash] = toAdd

#Check if position is winning for you
def isWin(hand: set[int], stones: int, matrix: dict[dict, dict[str, set[int]]], oppHand: set[int], turn: bool) -> set[int]:
    #print("Checking win with hand", hand, "stones", stones, "oppHand", oppHand)
    global hashUsed
    global nonHashUse
    hashableHand = hashableSet(hand)
    hashableOppHand = hashableSet(oppHand)
    if stones in matrix and hashableHand in matrix[stones] and hashableOppHand in matrix[stones][hashableHand]:
        hashUsed += 1
        return matrix[stones][hashableHand][hashableOppHand]
    nonHashUse += 1
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
            newHand = reduceHand(targetStones, playerHand)
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

def checkDone(matrix, stones, currentHand, currentOppHand):
    hashableHand = hashableSet(currentHand)
    hashableOppHand = hashableSet(currentOppHand)
    if stones in matrix:
        if hashableHand in matrix[stones]:
            if hashableOppHand in matrix[stones][hashableHand]:
                #print("Done!" )
                return True
    #print("Not Done", matrix)
    return False

def reduceHand(stones: int, hand: set[int]):
    return {card for card in hand if card <= stones}

def handCondition(turn, myHand, oppHand):
    return (turn and len(oppHand) - len(myHand) in {2,1}) or (not turn and len(myHand) == len(oppHand))
    
def checkNewCard(playerHandSet: set[int], otherPlayerHandSet: set[int], stones: int, maxStones: int, matrix, turn, newCard):
    newPlayerHand = playerHandSet.copy()
    newPlayerHand.add(newCard)
    newPlayerHand = reduceHand(stones, newPlayerHand)
    #print("NewPlayerHand: ", newPlayerHand)
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

def getMatrix(maxStones: int, cards: int, currentHand: set[int], currentOppHand: set[int], starting: bool):
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
getMatrix(20, 10, set([1,2,3,5,4,6,8]), set([1,2,5,8,7,9,3]), True)
print("hashUsed", hashUsed, "non-hashUse", nonHashUse)
print("--- Program finished in %s seconds ---" % (time.time() - startTime))

"""
Solution: 5, 6 or 7

If i play 5,
getMatrix
"""





        



            
                
    

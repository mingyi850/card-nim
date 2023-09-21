import time
import math

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
    #if oppHash not in matrix[stones][yourHash]:
    #    matrix[stones][yourHash][oppHash] = dict()
    matrix[stones][yourHash][oppHash] = toAdd

def getMoveset(stones, maxCards, playerUsedCards, oppUsedCards):
    allCardsOriginal = set(range(1, min(range(stones))))
    allCards = set(range(1, min(maxCards, stones) + 1))
    playerCards = allCards.difference(playerUsedCards)
    oppCards = allCards.difference(oppUsedCards)
    #print(stones, maxCards, playerUsedCards, oppUsedCards, playerCards, oppCards)
    breakingMoves = [stones - x for x in oppUsedCards if (stones - x) <= max(oppCards) and (stones - x) in playerCards] #moves that minimise 'safe' moves for opponent
    completeDefence = [card for card in playerCards if max(playerUsedCards.union({card})) < (stones - max(oppCards)) / 2]
    completeSet = set(completeDefence)
    partialDefence = [card for card in playerCards if card < (stones - max(oppCards)) and card not in completeSet]
    
    return breakingMoves, completeDefence, partialDefence

def allowDepth(maxCards, depth, type): #max allowed depth is always odd (opp turn)
    branchingFactor = maxCards
    computationLimit = 7000000
    divisor = math.log2(branchingFactor)
    if divisor == 0:
        divisor = 1
    allowedDepth = math.log2(computationLimit) // divisor
    if type == 'breaking':
        return depth <= 2 * allowedDepth - 1 or depth % 2 == 1
    else:
        if allowedDepth % 2 == 0:
            return depth <= allowedDepth - 1 or depth % 2 == 1
        else:
            return depth <= allowedDepth or depth % 2 == 1
        
cache = dict()
cacheHit = 0
computations = 0
def solve(stones, maxCards, playerUsedCards, oppUsedCards, turn, depth):
    global cache
    global cacheHit
    global computations
    computations += 1
    hashablePlayerUsed = hashableSet(playerUsedCards)
    hashableOppUsed = hashableSet(oppUsedCards)
    #print("Exploring state ", stones, playerUsedCards, oppUsedCards)
    if stones in cache and hashablePlayerUsed in cache[stones] and hashableOppUsed in cache[stones][hashablePlayerUsed]:
        cacheHit += 1
        return cache[stones][hashablePlayerUsed][hashableOppUsed]
    allCards = set(range(1, maxCards + 1))
    playerCards = allCards.difference(playerUsedCards)
    oppCards = allCards.difference(oppUsedCards)
    #playedMoves = set()
    if stones in playerCards:
        addToMatrix(stones, playerUsedCards, oppUsedCards, set({stones}), cache)
        return set({stones})
    elif stones < min(playerCards):
        addToMatrix(stones, playerUsedCards, oppUsedCards, set(), cache)
        return set()
    elif min(oppCards) > stones and min(playerCards) <= stones:
        return set({min(playerCards)})
    #print("Checking moveset for", stones, playerCards, oppCards)
    breaking, complete, partial = getMoveset(stones, maxCards, playerUsedCards, oppUsedCards)
    #print(breaking, complete, partial)
    if not breaking and not complete and not partial:
        return set()
    allowBreaking = allowDepth(len(breaking) + len(complete) + len(partial), depth, 'breaking')
    allowOther = allowDepth(len(breaking) + len(complete) + len(partial), depth, 'other')
    if allowBreaking:
        for move in breaking:
            #print("BREAKING", move)
            oppSolution = solve(stones - move, maxCards, oppUsedCards, playerUsedCards.union({move}), not turn, depth + 1)
            if not(oppSolution):
                addToMatrix(stones, playerUsedCards, oppUsedCards, set({move}), cache)
                return set({move})
        if allowOther:
            for move in complete:
                oppSolution = solve(stones - move, maxCards, oppUsedCards, playerUsedCards.union({move}), not turn, depth + 1)
                if not(oppSolution):
                    addToMatrix(stones, playerUsedCards, oppUsedCards, set({move}), cache)
                    return(set({move}))
            for move in partial:
                oppSolution = solve(stones - move, maxCards, oppUsedCards, playerUsedCards.union({move}), not turn, depth + 1)
                if not(oppSolution):
                    addToMatrix(stones, playerUsedCards, oppUsedCards, set({move}), cache)
                    return(set({move}))
    if allowBreaking and allowOther:
        addToMatrix(stones, playerUsedCards, oppUsedCards, set(), cache)
    # Loss mitigation scenarios
    if depth > 0:
        return set({})
    else:
        if complete:
            return set({-max(complete)})
        elif partial:
            return set({-max(partial)})
    
    

startTime = time.time()
stones = 23
maxCards = 9
print("Game with stones, cards:", stones, maxCards)
soln = getMoveset(stones, maxCards, set({}), set({}))
print(soln)
print("Depth restriction", allowDepth(maxCards, 11, 'branching'))
print("FIRST MOVE", solve(stones, maxCards, set({}), set({}), True, False))
#print("SECOND MOVE", solve(14, maxCards, set({}), set({9}), False, False))
#print(solve(15, maxCards, set({1}), set({3}), False, False))
#print(solve(12, maxCards, set({3}), set({1,3}), False, False))
print("cacheHits:", cacheHit)
print("computations:", computations)
print("--- Program finished in %s seconds ---" % (time.time() - startTime))
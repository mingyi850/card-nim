import time

def getMoveset(stones, maxCards, playerUsedCards, oppUsedCards):
    allCards = set(range(1, maxCards + 1))
    playerCards = allCards.difference(playerUsedCards)
    oppCards = allCards.difference(oppUsedCards)
    breakingMoves = [stones - x for x in oppUsedCards if (stones - x) < maxCards and (stones - x) not in playerUsedCards]
    completeDefence = [card for card in playerCards if max(playerUsedCards.union({card})) < (stones - max(oppCards)) / 2]
    partialDefence = [card for card in playerCards if card < (stones - max(oppCards)) / 2]
    return breakingMoves, completeDefence, partialDefence
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

cache = dict()
cacheHit = 0
def solve(stones, maxCards, playerUsedCards, oppUsedCards, turn):
    global cache
    global cacheHit
    hashablePlayerUsed = hashableSet(playerUsedCards)
    hashableOppUsed = hashableSet(oppUsedCards)
    print("Exploring state ", stones, playerUsedCards, oppUsedCards)

    if stones in cache and hashablePlayerUsed in cache[stones] and hashableOppUsed in cache[stones][hashablePlayerUsed]:
        cacheHit += 1
        return cache[stones][hashablePlayerUsed][hashableOppUsed]
    allCards = set(range(1, maxCards + 1))
    playerCards = allCards.difference(playerUsedCards)
    oppCards = allCards.difference(oppUsedCards)
    playedMoves = set()
    if stones in playerCards:
        addToMatrix(stones, playerUsedCards, oppUsedCards, set({stones}), cache)
        return set({stones})
    elif stones < max(playerCards):
        addToMatrix(stones, playerUsedCards, oppUsedCards, set(), cache)
        return set()
    
    breaking, complete, partial = getMoveset(stones, maxCards, playerUsedCards, oppUsedCards)
    for move in breaking:
        oppSolution = solve(stones - move, maxCards, oppUsedCards, playerUsedCards.union({move}), not turn)
        if not(oppSolution):
            addToMatrix(stones, playerUsedCards, oppUsedCards, set({move}), cache)
            return set({move})
        else:
            playedMoves.add(move)
    for move in [move for move in complete if move not in playedMoves]:
        oppSolution = solve(stones - move, maxCards, oppUsedCards, playerUsedCards.union({move}), not turn)
        if not(oppSolution):
            addToMatrix(stones, playerUsedCards, oppUsedCards, set({move}), cache)
            return(set({move}))
        else:
            playedMoves.add(move)
    for move in [move for move in partial if move not in playedMoves]:
        oppSolution = solve(stones - move, maxCards, oppUsedCards, playerUsedCards.union({move}), not turn)
        if not(oppSolution):
            addToMatrix(stones, playerUsedCards, oppUsedCards, set({move}), cache)
            return(set({move}))
        else:
            playedMoves.add(move)
    addToMatrix(stones, playerUsedCards, oppUsedCards, set(), cache)
    return set()
    

startTime = time.time()
stones = 101
maxCards = 20
soln = getMoveset(stones, maxCards, set(), set())
print(soln)
print(solve(stones, maxCards, set(), set(), True))
print("cacheHit:", cacheHit)
print("--- Program finished in %s seconds ---" % (time.time() - startTime))
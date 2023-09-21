import sys
import socket
import time
import math

class Client():
    def __init__(self, port=4000):
        self.socket = socket.socket()
        self.port = port

        self.socket.connect(("localhost", port))

        # Send over the name
        self.socket.send("Python Client".encode("utf-8"))

        # Wait to get the ready message, which includes whether we are player 1 or player 2
        # and the initial number of stones in the form of a string "{p_num} {num_stones}"
        # This is important for calculating the opponent's move in the case where we go second
        init_info = self.socket.recv(1024).decode().rstrip()

        self.player_num = int(init_info.split(" ")[0])
        self.num_stones = int(init_info.split(" ")[1])
        self.num_cards = int(init_info.split(" ")[2])

        self.anchor = self.num_stones
        self.myHand = list(range(1,self.num_cards+1))
        self.opHand = list(range(1,self.num_cards+1))
        

    def getstate(self):
        '''
        Query the server for the current state of the game and wait until a response is received
        before returning
        '''

        # Send the request
        self.socket.send("getstate".encode("utf-8"))

        # Wait for the response (hangs here until response is received from server)
        state_info = self.socket.recv(1024).decode().rstrip()

        # Currently, the only information returned from the server is the number of stones
        num_stones = int(state_info)

        return num_stones

    def sendmove(self, move):
        '''
        Send a move to the server to be executed. The server does not send a response / acknowledgement,
        so a call to getstate() afterwards is necessary in order to wait until the next move
        '''

        self.socket.send(f"sendmove {move}".encode("utf-8"))


    def generatemove(self, state):
        '''
        Given the state of the game as input, computes the desired move and returns it.
        NOTE: this is just one way to handle the agent's policy -- feel free to add other
          features or data structures as you see fit, as long as playgame() still runs!
        '''

        raise NotImplementedError

    def playgame(self):
        '''
        Plays through a game of Card Nim from start to finish by looping calls to getstate(),
        generatemove(), and sendmove() in that order
        '''

        while True:
            state = self.getstate()

            if int(state) <= 0:
                break

            move = self.generatemove(state)

            self.sendmove(move)

            time.sleep(0.1)

        self.socket.close()


class IncrementPlayer(Client):
    '''
    Very simple client which just starts at the lowest possible move
    and increases its move by 1 each turn
    '''
    def __init__(self, port=4000):
        super(IncrementPlayer, self).__init__(port)
        self.i = 0

    def generatemove(self, state):
        to_return = self.i
        self.i += 1

        return to_return

class MyPlayer(Client):
    '''
    Your custom solver!
    '''
    def __init__(self, port=4000):
        super(MyPlayer, self).__init__(port)
    
    def hashableSet(self, original):
        return ','.join([str(i) for i in sorted(list(original))])

    def toSet(self, hashed):
        if not hashed:
            return set()
        return set([int(x) for x in hashed.split(',')])

    def addToMatrix(self, stones, yours, opps, toAdd, matrix):
        yourHash = self.hashableSet(yours)
        oppHash = self.hashableSet(opps)
        if stones not in matrix:
            matrix[stones] = dict()
        if yourHash not in matrix[stones]:
            matrix[stones][yourHash] = dict()
        matrix[stones][yourHash][oppHash] = toAdd

    def getMoveset(self, stones, maxCards, playerUsedCards, oppUsedCards):
        allCards = set(range(1, min(maxCards, stones) + 1))
        playerCards = allCards.difference(playerUsedCards)
        oppCards = allCards.difference(oppUsedCards)
        #print(stones, maxCards, playerUsedCards, oppUsedCards, playerCards, oppCards)
        breakingMoves = [stones - x for x in oppUsedCards if (stones - x) <= max(oppCards) and (stones - x) in playerCards] #moves that minimise 'safe' moves for opponent
        completeDefence = [card for card in playerCards if max(playerUsedCards.union({card})) < (stones - max(oppCards)) / 2]
        completeSet = set(completeDefence)
        partialDefence = [card for card in playerCards if card < (stones - max(oppCards)) and card not in completeSet]
        
        return breakingMoves, completeDefence, partialDefence

    def allowDepth(self, maxCards, depth, type): #max allowed depth is always odd (opp turn)
        branchingFactor = maxCards
        computationLimit = 500000
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
    
    def solve(self, stones, maxCards, playerUsedCards, oppUsedCards, turn, depth, cache):
        hashablePlayerUsed = self.hashableSet(playerUsedCards)
        hashableOppUsed = self.hashableSet(oppUsedCards)
        #print("Exploring state ", stones, playerUsedCards, oppUsedCards)
        if stones in cache and hashablePlayerUsed in cache[stones] and hashableOppUsed in cache[stones][hashablePlayerUsed]:
            cacheHit += 1
            return cache[stones][hashablePlayerUsed][hashableOppUsed]
        allCards = set(range(1, maxCards + 1))
        playerCards = allCards.difference(playerUsedCards)
        oppCards = allCards.difference(oppUsedCards)
        #playedMoves = set()
        if stones in playerCards:
            self.addToMatrix(stones, playerUsedCards, oppUsedCards, set({stones}), cache)
            return set({stones})
        elif stones < min(playerCards):
            self.addToMatrix(stones, playerUsedCards, oppUsedCards, set(), cache)
            return set()
        elif min(oppCards) > stones and min(playerCards) <= stones:
            return set({min(playerCards)})
        #print("Checking moveset for", stones, playerCards, oppCards)
        breaking, complete, partial = self.getMoveset(stones, maxCards, playerUsedCards, oppUsedCards)
        #print(breaking, complete, partial)
        if not breaking and not complete and not partial:
            return set()
        allowBreaking = self.allowDepth(len(breaking) + len(complete) + len(partial), depth, 'breaking')
        allowOther = self.allowDepth(len(breaking) + len(complete) + len(partial), depth, 'other')
        if allowBreaking:
            for move in breaking:
                #print("BREAKING", move)
                oppSolution = self.solve(stones - move, maxCards, oppUsedCards, playerUsedCards.union({move}), not turn, depth + 1)
                if not(oppSolution):
                    self.addToMatrix(stones, playerUsedCards, oppUsedCards, set({move}), cache)
                    return set({move})
            if allowOther:
                for move in complete:
                    oppSolution = self.solve(stones - move, maxCards, oppUsedCards, playerUsedCards.union({move}), not turn, depth + 1)
                    if not(oppSolution):
                        self.addToMatrix(stones, playerUsedCards, oppUsedCards, set({move}), cache)
                        return(set({move}))
                for move in partial:
                    oppSolution = self.solve(stones - move, maxCards, oppUsedCards, playerUsedCards.union({move}), not turn, depth + 1)
                    if not(oppSolution):
                        self.addToMatrix(stones, playerUsedCards, oppUsedCards, set({move}), cache)
                        return(set({move}))
        if allowBreaking and allowOther:
            self.addToMatrix(stones, playerUsedCards, oppUsedCards, set(), cache)
        # Loss mitigation scenarios
        if depth > 0:
            return set({})
        else:
            if complete:
                return set({-max(complete)})
            elif partial:
                return set({-max(partial)})
            
    def generatemove(self, state):

        if state < self.anchor:
            # opponent made a move
            self.opHand.remove(self.anchor - state)

        result = self.solve(state, self.myHand, self.opHand)
        if result:
            move = math.abs(list(result)[0])
        else:
            move = max(self.myHand)
        self.myHand.remove(move)
        self.anchor = state - move

        return move
    
    def act(self, s, myHand, opHand):
        return 0



if __name__ == '__main__':
    if len(sys.argv) == 1:
        port = 4000
    else:
        port = int(sys.argv[1])

    # Change IncrementPlayer(port) to MyPlayer(port) to use your custom solver
    client = MyPlayer(port)
    client.playgame()


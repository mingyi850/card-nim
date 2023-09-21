# simulate only 2 steps into the future, act based on probability of winning
from bisect import bisect_left
import random
import time
random.seed(48)

def simulate_three_step(s, myHand, opHand): # choose actions to force opponent to lose
    # tries to incorporate third step
    if s > myHand[-1] + opHand[-1] + myHand[-1]:
        return random.choice(myHand)
    if s in myHand:
        return s
    if myHand[0] > s:
        # all cards exceed s
        return myHand[0] 
    
    best_index = bisect_left(myHand, s)-1
    min_lose_cnt, best_hand = 1e3, myHand[best_index]
    for i in range(best_index,-1,-1):
        hand = myHand[i]
        if hand > s: # avoid using cards that exceed s
            continue
        if hand <= 3 and min_lose_cnt < 1e3: # avoid using small cards if possible
            break
        win_count, lose_count = 0,0
        temp_myHand = myHand.copy()
        temp_myHand.remove(hand)
        op_action = simulate_two_step(s-hand, opHand, temp_myHand)
        if hand + op_action > s:
            return hand
        elif hand + op_action == s:
            continue
        else:
            for j in range(len(myHand)-1,-1,-1):
                sec_hand = myHand[j]
                if sec_hand == hand:
                    continue
                if hand + op_action + sec_hand > s:
                    lose_count += 1
                elif hand + op_action + sec_hand == s:
                    win_count += 1

        print(hand, win_count, lose_count, "three step")
        if win_count > 0: # choose actions if it can lead to win when opponent plays optimally
            return hand
        
        if lose_count < min_lose_cnt:
            best_hand = hand
            min_lose_cnt = lose_count
    return best_hand

def simulate_two_step(s, myHand, opHand): # choose action to survive after two steps
    # s is number of stones left
    # myHand is an array of cards in my hand
    # opHand is an array of cards in opponent's hand
    
    if s > myHand[-1] + opHand[-1]:
        return random.choice(myHand)
    if s in myHand:
        return s
    if myHand[0] > s:
        # all cards exceed s
        return myHand[0] 
    
    best_index = bisect_left(myHand, s)-1
    max_prob, max_hand = -1, myHand[best_index]
    for i in range(best_index,-1,-1):
        hand = myHand[i]
        if hand > s:
            continue
        win_count, lose_count = 0,0
        for op_hand in opHand:
            if hand + op_hand > s:
                win_count += 1
            elif hand + op_hand == s:
                lose_count += 1

        # print(hand, win_count, lose_count, "two step")

        if lose_count == 0: # choose actions that will not lead to a loss if possible
            return hand
        
        prob = win_count / (win_count + lose_count) if win_count + lose_count > 0 else 0
        if prob > max_prob:
            max_prob, max_hand = prob, hand
    
    return max_hand

s = 50
k = 15
myHand = list(range(1,k+1))
opHand = list(range(1,k+1))
my_turn = False
total_time = 0

while s>0:
    if my_turn:
        startTime = time.time()
        hand = simulate_three_step(s, myHand, opHand)
        total_time += (time.time() - startTime)
        myHand.remove(hand)
        s -= hand
        print("I played", hand, "stones.", s, "stones left. I have",' '.join(map(str, myHand)), "cards left. You have", ' '.join(map(str, opHand)), "cards left.")
    else:
        print("Your turn. Please play.")
        hand = int(input())
        while hand not in opHand:
            print("Please play a valid card.")
            hand = int(input())
        opHand.remove(hand)
        s -= hand
        print("You played", hand, "stones.", s, "stones left. I have",' '.join(map(str, myHand)), "cards left. You have", ' '.join(map(str, opHand)), "cards left.")

    if s == 0:
        if my_turn:
            print("I won!")
        else:
            print("You won.")
    elif s<0:
        if my_turn:
            print("You won.")
        else:
            print("I won!")

    my_turn = not my_turn
    print()

print("Took me", total_time, "seconds.")
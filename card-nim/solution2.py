# simulate only 2 steps into the future, act based on probability of winning
import random
import time
random.seed(48)

def simulate_three_step(s, myHand, opHand):
    # tries to incorporate third step
    if s > len(myHand) + len(opHand) + len(myHand):
        return random.choice(myHand)
    if s in myHand:
        return s
    
    max_prob, max_hand = -1,random.choice(myHand)
    for i in range(len(myHand)-1,-1,-1):
        hand = myHand[i]
        if hand > s:
            continue
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

        # if lose_count == 0: # choose actions that will not lead to a loss if possible
        #     return hand
        
        prob = win_count / (win_count + lose_count) if win_count + lose_count > 0 else 0
        if prob > max_prob:
            max_prob, max_hand = prob, hand
        print(hand, win_count, lose_count, prob)
    return max_hand

def simulate_two_step(s, myHand, opHand):
    # s is number of stones left
    # myHand is an array of cards in my hand
    # opHand is an array of cards in opponent's hand
    
    if s > len(myHand) + len(opHand):
        return random.choice(myHand)
    if s in myHand:
        return s
    
    max_prob, max_hand = -1,random.choice(myHand)
    for i in range(len(myHand)-1,-1,-1):
        hand = myHand[i]
        if hand > s:
            continue
        win_count, lose_count = 0,0
        for op_hand in opHand:
            if hand + op_hand > s:
                win_count += 1
            elif hand + op_hand == s:
                lose_count += 1

        if lose_count == 0: # choose actions that will not lead to a loss if possible
            return hand
        
        prob = win_count / (win_count + lose_count) if win_count + lose_count > 0 else 0
        if prob > max_prob:
            max_prob, max_hand = prob, hand
        # print(hand, win_count, lose_count, prob)
    return max_hand

s = 300
k = 25
myHand = list(range(1,k+1))
opHand = list(range(1,k+1))
my_turn = True
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
            print("You won!")
    elif s<0:
        if my_turn:
            print("You won!")
        else:
            print("I won!")

    my_turn = not my_turn
    print()

print("Took me", total_time, "seconds.")
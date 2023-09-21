Variables to track
1. Who's turn it is
2. Number of stones left: s
3. Cards in your hand: list from 1..k with skips
4. Cards in Opponents hand

Constraints 
1. (sum(1..k) > s)
2. At any given turn, cards in my hand (n) = n' (I Start first) or = n'-1 (opponent starts first)


Base case:

s = 1
each player has 1 
My turn: i win, opponent's turn, she wins

s = 2
each player has 1
my turn: i lose, opponent's turn, she loses

s = 2
Each player has 2
my turn: i win, opponent's turn, she win
- I have 1 and 2, opponent has 1
my turn: i win, opponent's turn, she loses
- I have 2, opponent has 1 and 2
my turn, i win, opponent's turn, she wins
- I have 1, opponent has 1 and 2
Either way i lose

Rules: 
1. If i have card s in my hand on my turn i win, likewise for my opponent
2. If all cards in my hand are more than remaining stones, I lose. Likewise for my opponent

Strategies:
1. We need to find a way to Force defeat for the opponent
2. Make remaining value equal to a card that the opponent has played. Extra points if the remainder is > the card you played.
3. I want to play the highest number where opponent cannot get me down to that particular number immediately
4. S - highest card - remainder > highest card player has played - this is winning.
Can we play it like NIM? Keep the total to be some multiple above my lowest card 


Example:
s = 50
k = 30

Opp starting case
Opp plays 19  Opp plays 15              Opp plays 10           Opp Plays 10 (40)     Opp plays 9 (41)    Opp plays 9 (41)                   Opp plays 9 (41) Opp Max = 30               
I play 12     I play 20                 I play 30              I play 30 (10)        I play 7 (34)       I play 3 (38)                      I play 4 (37) 
opp plays 7   Opp loses no matter what  Opp Loses regardless   Opp plays             Opp plays 27 (7)    Opp plays 2 (36)                   Opp plays 3 (34)
I play 5                                                                             I play              I play 27 (9)                      I play 25 (9)
opp plays 2                                                                                              Opp plays 6 (3)                    Opp plays 5 (4)
I play 3                                                                                                 I play 1 (2)                       I play 1 (3)
opp plays 1                                                                                              Opp plays 1 (1) And I lose still   Opp plays 2 (1) (I lose)
I win.

Continued
s = 20
k = 6

Opp plays 6 (14)
I play 6 (8)
2 options: break 5 ( highest card i have) or don't break. Since highest card i played i higher than 5, if he breaks 5 he will lose
So, he can either play to 6, 7
Case 1: Play to 6
    Opp plays 2 (6)
    Anything i play will break 5, so only safe option is to play to 2 (since opponent has played it)
    I play 3 (2)
    Opp loses (either play 1 or 3, after he plays 1 i play 1)
Case 2:
    Opp plays 1 (7)
    I can either not break (play to 6 or play to 1)
    If I play to 1, opp loses since he does not have 1
    If I play to 6:
        I play 1 (6)
    Opp has to break 5 regardless, so opp can play 2, 3, 4, 5
    Since I have played 1, opp can play 5 to force me to 1, and make me lose.

So classically, we should have a 3D array for dynamic programming here to decide on win and loss states
1. We should construct the 3d matrix of winning and losing states
2. Then, keep moving opponent into state with 0 winning states. 
3. If we are in losing state, we want to move to a state with the most possibilities for winning
4. If we are in winning state (state with 1 or more confirmed winning paths), stay in winning state

Construct player start matrix
s = 20, n = 6

(1, 1, 1) <- Win score = 100 ( This is great, we start from here) -> Iterate through all cards from 2 to n and calculate win score.
(3, 1, 12) <- Win score = 0
(4, 1, 13) <- Win score = 0
(5, 1, 14) <- Win score = 0
...
(7, 1, 16) <- Win score = 0
....
(2, 1, 1) <- Win score = 0
(2, 1, 2) <- Win score = 100
(2, 1, 3) <- Win score = 100
...
(2, 1, 6) <- Win score = 100

(5, 12, 12) <- Win score = 100
(5, 13, 12) <- Win score = 100
(6, 14, 12) <- Win score = 100
...
(13, 16, 16) <- Win score = 100


(1, 12, 12) <- Win score = 100
...
(1, 123456, 123456) <- Win score = 100
(1, 2, 2) <- Win score = 0
...
(1, 23456) <- Win score = 0
..
(1, 6) <- Win score = 0
(2, 1, 1) <- Win score = 0
(2, 12, 12) <- Win score = 100
(2, 123, 123...) <- Win score = 100

Win score = -Score(s - card, hand - card, opp hand) where card in hand

Air bubbles
30 10 10

Move set:
 1-10 ->  
 Play 20: 20, 9, 10

 I play, 10, opp plays 10. Game becomes 10, 9 ,9 (I lose)
 I play 9, opp plays 10, Game becomes 11, 1-8,10, 9
 I can play 1 to bring game to 10, 2-8, 9
 Opp can crush me with 9
I play 8, opp plays 10, Game becomes  
 
2 options: 
if i can get it to a card that opponent has played
e.g 1-27, 28-40, 1-40, 50  
I have 2 options:
1. Get it to card that opp has played
2. Get it to card above (max(opp))

Case 1: opp has played 27, I want to get it down to 27 so i play 23
Now we can simulate the forced moves. Opp plays 4 -> 23 
27, 1-26, 1-22, 24-26
23, {27, 4}, 1-3,5-23 1-22,24-26
4, {27, 4}, 1-3,5-23 1-3
I play 19 -> 4
Scenario: If I can break opponent by playing a card < break number: simulate till the end via force moves
Scenario: If i can break opponent by playing a card > break number: I will win.

Case 2: Say we are unable to break opponent (there is no winning hand to break):
I need to trim the remainder down to a level above the break point (40 i.e max(opp))
Available cards: 1-9 
How do i choose from available cards? Is this a subproblem? (Already kinda easy in this case since there are only 9 subproblems to solve.)

force opponent to break: play 9
41 {27} {9}
Opp has 1 moves - get it to 9
Opp plays 32
9 {32, 27}, {9}
Anything i play, opp can counter so i will lose

force opponent to break: play 8
42 {27} {8}
Opp has 1 moves - get it to 8 or get it to 41
Opp plays 33
8 {33, 27}, {8}
Anything i play, opp can counter so i will lose
Again, i am screwed. Opp can play BREAK with (card > myCard)
Even if i play 4
45 {27} {4}
Opp can get it down to 1 

To not break: Have to play card such that max(opp) + card > stones - card i.e (max(opp)) + 2(card) < stones 
card < (stones - max(opp)) / 2
I play 4
46 {27},{4}
Opp cannot get it down to 4. 
Opp has to play card such that max(me) + 2(max(card_played)) > stones. In this case, he has to play card 1 or 2
Opp plays 1
45 {1}, {4}
Here i cannot get it down to 1, (assuming no break) so i can play nothing - everything 1 do will break 4 (stones - 40) / 2 = 2.5 < 4
But i can play {1,2,3(?)} to start breaking chains.

43 {1} {2, 4}
Opp can break to 4.
4 {1}, {2,4}
I can play 3.
1 {1}, {2,3,4} -> opp has used 1, i win.

44 {1} {1,2,4}
Opp can break to 4.
4 {1}, {1,2,4}
I can play 3 -> opp has used 1, i win.
Only break iff player has card in hand for which for each card in opp hand, I have not used reciprocal.

42 {1} {4, 3}
Opp can break to 4 or 3
Opp breaks to 4 -> because for all cards in my hand (1,2), Opp has not used reciprocal (2,3) -> OPP WIN
Opp breaks to 3 -> for card in my hand (1,2), opp has to have both 1,2 to survive. Here, he does not have 1 so he will lose.

Moveset: 
1. Breaking moves
2. Defensive moves (Complete defence)
3. Minimising defence
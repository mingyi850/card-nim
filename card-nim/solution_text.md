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

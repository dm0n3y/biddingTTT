This folder contains my final project for CS373 (Artificial Intelligence)
at Williams College.  Partners were Kevin Chen '15 and Patrick Johnson '15.
Topic was independently chosen.

In this project, we implemented in Python perfect players of bidding Tic 
Tac Toe.  A bidding game is a standard 2-person turn-based game (e.g. 
chess, Connect Four, Tic Tac Toe, etc.) in which players start with some 
number of chips, and, at each turn, must bid some non-negative amount for 
the right to move.  The winning bidder gets to move, but at the expense of 
giving her winning bid to her opponent.  So there is a delicate balance 
between bidding enough to make your move, and bidding too much and giving 
your opponent too many chips.  See 'BiddingChess.pdf' in the 'Reading' 
folder for a more detailed introduction.

All of the code can be found in the file 'TTT.py'.  The 'Distance_' and 
'TTTLegalStates.txt' files are there to facilitate generating the winning 
strategy.  

We also implemented a basic game engine that allows users to play against 
our players.  To play, simply run the 'TTT.py' file at the command line.

We have two perfect players: one for real-valued bidding Tic Tac Toe, and 
another for discrete-valued bidding Tic Tac Toe (e.g. bidding with chips).  
Our real-valued bidding player is implemented using the theory of the late 
David Richman.  Richman introduced the idea of bidding games in the late 
1980's.  In particular, he drew a fascinating connection between real-
valued bidding games and random-turn-based games, in which players flip a 
coin at each turn to determine who gets to move.  Suppose Alice and Bob 
play a real-valued bidding game, and the total 'chip count' for both 
players is 1.  Given some gamestate G, let R(G) denote the minimum 'chip 
count' Alice must have in order to have a winning strategy from G.  Let 
P(G) denote the probability that Alice wins from G if it were henceforth 
played as a random-turn-based game.  The elegant Richman's Theorem states 
that R(G) = 1 - P(G).

Richman's Theorem and its proof also provide the means of determining a
perfect winning strategy for Alice, provided that Alice begins with R(G_0) 
chips, where G_0 is the starting gamestate.  This involves assigning 
R(G) = 0 for any gamestate G in which Alice has won, R(G) = 1 for any 
gamestate G in which Alice has lost or drawn, and backward-inducting from
those terminal gamestates to calculate R(G) for all other gamestates G.  
Once these values are calculated, Alice's optimal move is that which
minimizes R(G), and her optimal bid is half the difference between the
minimum and maximum of R(G), where the min and max are taken over all
gamestates G to which Alice can move from the current gamestate.  Again, 
see 'BiddingChess.pdf' in the 'Reading' folder for more details. 

Richman's theory has been extended to discrete-valued bidding games by 
Sam Payne and Mike Develin.  Their extension can be applied in a similar
fashion to implement a perfect strategy in discrete-valued bidding games
(again, assuming that the player starts with some minimum required number
of chips).  See 'DiscreteBiddingGames.pdf' in the 'Reading' folder for
the details of their work.





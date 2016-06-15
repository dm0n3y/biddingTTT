# biddingTTT
A perfect player of bidding Tic-Tac-Toe.  Developed together with Kevin Chen
  and Patrick Johnson. The winning strategy is implemented for both 
  real- and discrete-valued bidding using Richman's theory and extensions 
  thereof by Mike Develin and Sam Payne.


## Overview

The following is a very brief overview of bidding games and Richman's theory.  See
  [this article](http://arxiv.org/pdf/0903.2995.pdf)
  for a more detailed overview, and [this paper](https://arxiv.org/abs/0801.0579)
  by Develin and Payne for their extension of Richman's theory to discrete-valued 
  bidding.



### Bidding Games

Bidding games were introduced in the 1980s by the mathematician 
  David Richman.  A bidding game is an extension of any two-person 
  turn-based game, e.g.,
  chess, Connect Four, Tic-Tac-Toe, etc. In a bidding game, players 
  additionally maintain a finite supply of 
  chips and must bid them at every turn for the right to move.  The winning 
  bidder gets to move, but at the expense of paying the bidded 
  chips to the losing bidder. Players must navigate a delicate balance between
  bidding enoughto make a move, and bidding too much and giving the opponent too many chips.

The latter can have significant consequences.
For example, suppose Alice and Bob are playing bidding Connect Four.
If Alice is one move away from four-in-a-row and has more chips than Bob, 
  then she is guaranteed the winning move.
If Alice is two moves away from four-in-a-row and has more than triple Bob's chips,
  then she is guaranteed those two moves in succession.
In general, if Alice has more than (2<sup>k</sup>-1)-times Bob's chips, then 
  she is guaranteed k moves in succession (if so desired).
  



### Richman's Theory

Richman drew an elegant connection between real-valued bidding games, in which
any non-negative real value can be bid, and random-turn-based games, in which 
players flip a coin at each turn to determine who gets to move.  Suppose
Alice and Bob are playing a real-valued bidding game, where the total "chip
count" across both players is 1.  Given the current gamestate G, let R(G) 
denote the minimum "chip count" Alice must have in order to have a winning
strategy from G.  Let P(G) denote the probability that Alice wins from G if
it were henceforth played as a random-turn-based game.  Richman's Theorem
states that
<p align="center">
R(G) = 1 - P(G).
</p>
In other words, the less likely it is that 
Alice wins by chance, the more chips she needs for a winning strategy.

Richman's Theorem depends on the players being able to bid arbitrary non-negative
real values.  In the paper linked above, Devlin and Payne extend Richman's theory
to the more realistic situation in which players must bid non-negative integer
values, i.e., physical chips.


### Winning Strategy

Richman's Theorem itself can be used to generate a winning strategy.  At each
turn, Alice's optimal move is that which minimizes R(G).  If Alice has won
in G, then R(G) = 0, i.e., Alice needs no more chips to win.  Conversely,
if Alice has lost in G, then R(G) = 1.  Otherwise, if G is a non-terminal
gamestate, R(G) is computed recursively from the gamestates reachable from G
using Richman's Theorem.  Alice's optimal bid is half the difference between
the minimum and maximum of G.

A truly winning strategy requires the player to begin with slightly more than
half of the total chip count.  Numerical experiments suggest that this percentage
converges around 52%.  Hence, this player begins with a slight advantage in chip
count in order to ensure victory.


## To Play
To play, run `python TTT.py` in the project root directory.  Options for 
  real-/discrete-valued bidding, total chip count, and the
  tie-breaking chip will be presented.
  

# coop_wumpus
Our new approach aims to allow multiple agent approaches to work together on a wumpus environment.
An executable file in java - which can be fed with the locations of the files for two agents - will simulate one walkthrough in our
partially observable, strategic, sequential, static, discrete multiagent wumpus world.
wumpus world with gym env

based on:

https://github.com/Davood-M/gym_wumpus_world

how to:

https://www.novatec-gmbh.de/en/blog/creating-a-gym-environment/


# how to install

1. install gym 
```
pip install --upgrade gym==0.10.0
```
2. Install wumpus environment into pip
```
pip install -e .
```
3. execute train.py 
```
python train.py
```

# World description

### env
+ wumpus environment is rectangular
+ Agents: one or more wumpi, two Player
+ possible observations: nothing, gold, pit, breeze, stench, exit (mby light), locationvector for scream

### states
+ gold: contains one gold
+ pit: kills agent
+ breeze: in von Neumnann neighborhood to pit
+ stench: in von Neumnann neighborhood to wumpus
+ vector: pointing from one agents position to the scream location

### requirements
+ Rectangle: minimal size: |players|+2 for hight or width, the other side being at least |players| 
+ all gold has to be reachable

###### number of ...
+ ...pits: |players| + 1
+ ...gold: |wumpi|
+ ...wumpi: |gold|


# Actions

### Perception of the Player
Perception of a player is limited to the cell she is standing on (partially-observable)
This means the state of only this one cell is fixed but she is meant to remember the states of cells she has been to since they dont change a lot.

### actions of the player
- walk_up
  - the player can walk one cell every move
- walk_down
  - the player can walk one cell every move
- walk_left
  - the player can walk one cell every move
- walk_right
  - the player can walk one cell every move
- pick up
  - the player can pick up gold if she is on a gold cell
- put down
  - if the player has gold she can put it back on the ground
- climb
  - the wumpus cave has to be left climbing out the way the player entered
- scream
  - a scream can be heard by other players and will be represented as a vector
- nothing
  - do nothing for one turn

### goal
pick up a piece of gold and leave (asap?)

# coop_wumpus
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

## Wumpus World gym Environment
This package implements the famous wumpus world enviornment but with multiple agents and an agent wumpsu. Below you can see a sample loaded environment of the previous version.

```
#################################
#   .   |   .   |   .   |   .   #
#-------------------------------#
#   W   |   G   |   P   |   .   #
#-------------------------------#
#   .   |   .   |   .   |   .   #
#-------------------------------#
#   ^   |   .   |   P   |   .   #
#################################
```

The flash shows the agent, while 'W' shows the wumpus, 'P' indicates a pit, and 'G' shows the gold. The goal for the agent is to pickup the gold and get out of the maze from its entry point.

### Actions
The actions are as follow:
```
TurnRight: turns the agent's heading to right
TurnLeft: turns the agent's heading to left
Forward: the agent moves forward one step based on its current heading
Shoot: the agent shoots an arrow (has only 1 arrow)
Grab: grabs the gold if its on the agent's location
Climb: to get out of the cave when gold is acquired
```

### Rewards
The rewards are as follow:

```
-1: for each performed action
+1000: if the agent leaves with gold
-1000: if the agent dies (gets eaten by the wumpus or falls into a pit)
```

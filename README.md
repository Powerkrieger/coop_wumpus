# coop_wumpus
Our new approach aims to allow multiple agent approaches to work together on a wumpus environment.
An executable file in java - which can be fed with the locations of the files for two agents - will simulate one walkthrough in our
partially observable, strategic, sequential, static, discrete multiagent wumpus world.


# how to install
== TODO ==
```java
someting.func()
```
-
-

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
+ goal: collecting gold + (asap?)
+ vector: pointing from one agents position to the scream location
### requirements
+ Rectangle: minimal size: |players|+2 for hight or width, the other side being at least |players| 
+ all gold has to be reachable

###### number of ...
+ ...pits: |players| + 1
+ ...gold: |wumpi|
+ ...wumpi: |gold|


# Actions

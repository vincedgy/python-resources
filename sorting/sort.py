#!/usr/local/opt/python3/bin/python3
import sys
import math

# The while loop represents the game.
# Each iteration represents a turn of the game
# where you are given inputs (the heights of the mountains)
# and where you have to print an output (the index of the mountain to fire on)
# The inputs you are given are automatically updated according to your last actions.
montains = []
montains.append(1)
montains.append(2)
montains.append(4)
montains.append(3)
montains.sort()
print(montains[-1])

